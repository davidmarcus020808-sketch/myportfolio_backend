from django.apps import AppConfig
from django.conf import settings
import os

class PortfolioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_app'

    def ready(self):
        # Only run superuser creation in production or when explicitly allowed
        if os.environ.get("CREATE_SUPERUSER", "") == "True":
            from django.contrib.auth import get_user_model
            User = get_user_model()

            username = "DAVID"
            email = "davidmarcus020808@gmail.com"
            password = "Destinyekong6++"

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print("Superuser created!")
            else:
                print("Superuser already exists.")
