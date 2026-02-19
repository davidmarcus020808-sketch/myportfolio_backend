import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import ContactMessageSerializer
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer
from django.views.decorators.csrf import csrf_exempt  # <-- import this

# ------------------ CONTACT ENDPOINT ------------------
@csrf_exempt  # <-- add this
@api_view(["GET", "POST"])
def contact_view(request):
    # ------------------ Health Check ------------------
    if request.method == "GET":
        return Response(
            {"message": "Contact endpoint is live. Use POST to submit messages."},
            status=status.HTTP_200_OK,
        )

    data = request.data.copy()

    # ------------------ Honeypot Check ------------------
    if data.get("honeypot"):
        return Response(
            {"error": "Spam detected."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ------------------ reCAPTCHA Verification ------------------
    token = data.pop("recaptcha_token", None)
    if not token:
        return Response(
            {"error": "Please complete the reCAPTCHA."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Send token + secret to Google
    try:
        google_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": token,
            },
            timeout=5,
        ).json()
    except requests.RequestException:
        return Response(
            {"error": "Unable to verify reCAPTCHA."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # ------------------ Debug Logging ------------------
    print("=== Google reCAPTCHA Response ===")
    print(google_response)
    print("=================================")

    # Check if verification succeeded
    if not google_response.get("success", False):
        return Response(
            {
                "error": "reCAPTCHA verification failed.",
                "details": google_response.get("error-codes", []),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ------------------ Validate & Save Message ------------------
    serializer = ContactMessageSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    message = serializer.save()

    # ------------------ Send Email ------------------
    try:
        send_mail(
            subject=f"New Contact: {message.subject}",
            message=f"""
Name: {message.name}
Email: {message.email}
Phone: {message.phone or 'N/A'}

Message:
{message.message}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["davidmarcus020808@gmail.com"],
            fail_silently=False,
        )
    except Exception as e:
        print("Error sending email:", e)

    return Response(
        {"message": "Message sent successfully."},
        status=status.HTTP_201_CREATED,
    )

# ------------------ PROJECT ENDPOINTS ------------------
@api_view(["GET"])
def project_list(request):
    qs = Project.objects.prefetch_related("built").all()
    serializer = ProjectSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("built"), slug=slug)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
