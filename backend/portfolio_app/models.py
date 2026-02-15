from django.db import models
from django.utils.text import slugify


# ------------------ CONTACT ------------------
STATUS_CHOICES = [
    ("new", "New"),
    ("read", "Read"),
    ("replied", "Replied"),
]

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    honeypot = models.CharField(max_length=255, blank=True)
    email_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


CATEGORY_CHOICES = [
    ("personal", "Personal"),
    ("portfolio", "Portfolio"),
    ("business", "Business"),
    ("ecommerce", "E-commerce"),
    ("webapp", "Web Application"),
    ("education", "Education"),
    ("entertainment", "Entertainment"),
    ("ngo", "NGO"),
    ("news", "News"),
    ("social", "Social"),
    ("search", "Search Engine"),
]


class Project(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    video = models.FileField(upload_to="projects/videos/", blank=True, null=True)  # <-- NEW
    features = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.slug})"

    def save(self, *args, **kwargs):
        # auto-generate slug from title if not provided
        if not self.slug:
            base = slugify(self.title)[:90]
            slug = base
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class BuiltItem(models.Model):
    project = models.ForeignKey(Project, related_name="built", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="built_items/", blank=True, null=True)
    video = models.FileField(upload_to="built_items/videos/", blank=True, null=True)  # <-- NEW
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.project.slug})"