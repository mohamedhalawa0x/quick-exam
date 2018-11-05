from django.urls import path
from . import views

app_name = "courses"
urlpatterns = [
    path("", views.courses, name="courses"),
    path("<int:id>", views.chapters, name="chapters"),
]
