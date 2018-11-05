from django.contrib import admin
from .models import Course, Chapter, Question, Choice
from django.core.exceptions import ValidationError
from django import forms


# Validate Max of 12 Questions Allowed Per Chapter
class QuestionAdminForm(forms.ModelForm):
    def clean_objective(self):
        objective1 = self.cleaned_data['objective']
        if Question.objects.count() > 0:
            objectives_count = Question.objects.filter(
                objective=objective1).count()
            if objectives_count == 4:
                raise ValidationError(
                    'You Have Exceeded The maximum of number (4) of the Same objective'
                )
        return objective1

    def clean_chapter(self):
        chapter = self.cleaned_data['chapter']
        if chapter.question_set.exclude(pk=self.instance.pk).count() == 12:
            raise ValidationError('Max 12 Questions allowed!')
        return chapter


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm


# Validate Max of 3 Choices Allowed Per Questions
class ChoiceAdminForm(forms.ModelForm):
    def clean_chapter(self):
        question = self.cleaned_data['question']
        if question.question_set.exclude(pk=self.instance.pk).count() == 3:
            raise ValidationError('Max 3 Choices allowed!')
        return question


class ChoiceAdmin(admin.ModelAdmin):
    form = ChoiceAdminForm


# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
