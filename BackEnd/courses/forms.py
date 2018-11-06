from django import forms
from .models import Choice


class QuestionChoicesForm(forms.Form):
    options = forms.ChoiceField(widget=forms.RadioSelect, choices=[])

    def __init__(self, *args, **kwargs):
        choices_list = args[1]
        mytuple = tuple()
        for choice in choices_list:
            mytuple += ((choice.content, choice.content), )
        super(QuestionChoicesForm, self).__init__(*args, **kwargs)
        self.fields['options'].choices = mytuple
