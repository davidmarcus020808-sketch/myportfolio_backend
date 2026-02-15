from django.urls import path
from .views import contact_view, project_list, project_detail


urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path("projects/", project_list, name="project-list"),
    path("projects/<slug:slug>/", project_detail, name="project-detail"),
]
