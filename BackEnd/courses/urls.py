from django.urls import path
from . import views

app_name = "courses"
urlpatterns = [
    path("", views.courses, name="courses"),
    path("<int:id>", views.chapters, name="chapters"),
    path("<int:course_id>/<int:chapter_id>", views.exam, name="exam"),
]
