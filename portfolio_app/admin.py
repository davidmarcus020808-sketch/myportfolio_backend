from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from .models import ContactMessage, Project, BuiltItem


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "status",
        "created_at",
        "email_sent_at",
        "short_message",
    )

    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")

    # ✅ Only fields that actually exist in the model
    readonly_fields = ("created_at", "honeypot", "email_sent_at")

    actions = ["mark_as_read", "mark_as_replied"]

    def short_message(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    short_message.short_description = "Message Preview"

    def mark_as_read(self, request, queryset):
        updated = queryset.update(status="read")
        self.message_user(request, f"{updated} message(s) marked as Read.")
    mark_as_read.short_description = "Mark selected messages as Read"

    def mark_as_replied(self, request, queryset):
        sent_count = 0

        for message in queryset:
            if message.status == "replied":
                continue

            html_content = render_to_string(
                "emails/reply_email.html",
                {
                    "name": message.name,
                    "message": message.message,
                },
            )
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=f"Re: {message.subject}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[message.email],
            )
            email.attach_alternative(html_content, "text/html")

            try:
                email.send()
                message.status = "replied"
                message.email_sent_at = timezone.now()
                message.save()
                sent_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Failed to send email to {message.email}: {str(e)}",
                    level="error",
                )

        self.message_user(
            request,
            f"{sent_count} message(s) replied to and email(s) sent.",
        )
    mark_as_replied.short_description = "Mark selected messages as Replied and send email"

# admin.py
class BuiltItemInline(admin.TabularInline):
    model = BuiltItem
    extra = 1
    fields = ("title", "image", "video", "url")  # <-- include video

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "slug")
    inlines = [BuiltItemInline]
    fields = ("title", "slug", "category", "description", "image", "video", "features")
