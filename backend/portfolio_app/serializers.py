from rest_framework import serializers
from .models import ContactMessage, Project, BuiltItem


# ------------------ CONTACT ------------------
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "honeypot",
            "status",
            "created_at",
            "email_sent_at",
        ]
        read_only_fields = ["status", "created_at", "email_sent_at"]

# serializers.py

class BuiltItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()  # <-- NEW

    class Meta:
        model = BuiltItem
        fields = ["id", "title", "image", "video", "url"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.video and hasattr(obj.video, "url"):
            return request.build_absolute_uri(obj.video.url) if request else obj.video.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()  # <-- NEW
    built = BuiltItemSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "slug",
            "title",
            "category",
            "description",
            "image",
            "video",
            "features",
            "built",
            "created_at",
        ]

    def get_id(self, obj):
        return obj.slug

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.video and hasattr(obj.video, "url"):
            return request.build_absolute_uri(obj.video.url) if request else obj.video.url
        return None
