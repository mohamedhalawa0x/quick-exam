from django.shortcuts import render
from .models import Course, Chapter


# Create your views here.
def courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, "course/courses.html", context)


def chapters(request, id):
    course_obj = Course.objects.filter(id=id)[0]
    chapters = Chapter.objects.filter(course=id)
    context = {'chapters': chapters, 'course': course_obj}
    return render(request, "course/chapters.html", context)
