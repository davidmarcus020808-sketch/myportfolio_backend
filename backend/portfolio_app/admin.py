from django.contrib import admin
from .models import ContactMessage, Project, BuiltItem


# ------------------ CONTACT MESSAGE ADMIN ------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",  # keep field for reference, but no sending email
        "subject",
        "status",
        "created_at",
        "short_message",
    )
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at", "honeypot")

    actions = ["mark_as_read"]

    def short_message(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    short_message.short_description = "Message Preview"

    def mark_as_read(self, request, queryset):
        updated = queryset.update(status="read")
        self.message_user(request, f"{updated} message(s) marked as Read.")
    mark_as_read.short_description = "Mark selected messages as Read"


# ------------------ BUILT ITEM INLINE ------------------
class BuiltItemInline(admin.TabularInline):
    model = BuiltItem
    extra = 1
    fields = ("title", "image", "video", "url")


# ------------------ PROJECT ADMIN ------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "slug")
    inlines = [BuiltItemInline]
    fields = ("title", "slug", "category", "description", "image", "video", "features")
