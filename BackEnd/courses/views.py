from django.shortcuts import render
from .models import Course, Chapter, Question, Choice
from .forms import QuestionChoicesForm


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


def exam(request, course_id, chapter_id):
    questions = Question.objects.all()
    pre_context = prepare_questions_structure(request, questions)
    context = {'items': pre_context}
    return render(request, 'course/exam.html', context)


def get_question_choices(question_id):
    return Choice.objects.filter(question=question_id)


def prepare_questions_structure(request, questions):
    for question in questions:
        choices = get_question_choices(question.id)
        form = QuestionChoicesForm(request.POST or None, choices)
        yield {'Question': question, 'form': form}
