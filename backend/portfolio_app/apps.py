from django.apps import AppConfig
import os

class PortfolioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_app'

    def ready(self):
        # Only run this once, after migrations
        if os.environ.get("CREATE_SUPERUSER", "False") == "True":
            from django.contrib.auth import get_user_model
            User = get_user_model()

            SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
            SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
            SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "password123")

            if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
                print(f"Creating superuser: {SUPERUSER_USERNAME}")
                User.objects.create_superuser(
                    username=SUPERUSER_USERNAME,
                    email=SUPERUSER_EMAIL,
                    password=SUPERUSER_PASSWORD
                )
