from django.forms import ModelForm, RadioSelect
from .models import Quiz
from django.utils.translation import gettext_lazy as _


class QuizForm_1(ModelForm):
    class Meta:
        model = Quiz
        fields = ['dist','age', 'gender', 'negative_effect', 'previously_suffered', 'currently_experiencing_symptoms']
        labels = {
            'dist': _('Choose Your District '),
            'age': _('Under which age-group do you fall in?'),
            'gender': _('You identify yourself to which gender?'),
            'negative_effect': _('Is the Lockdown having any negative effect on your mental health?'),
            'previously_suffered': _('Have you previously ever suffered from depression, anxiety or any other mental health condition?'),
            'currently_experiencing_symptoms': _('Do you feel you are currently experiencing any symptoms of depression, anxiety or any other mental health condition?')
        }
        widgets = {
            'age': RadioSelect(),
            'gender': RadioSelect(),
            'negative_effect': RadioSelect(),
            'previously_suffered': RadioSelect(),
            'currently_experiencing_symptoms': RadioSelect(),
        }


class QuizForm_2(ModelForm):
    class Meta:
        model = Quiz
        fields = ['feelings_due_to_lockdown', 'therapist']
        labels = {
            'feelings_due_to_lockdown': _('Are these feelings due to enforcement of lockdown?'),
            'therapist': _('Have you tried talking to any therapist or reached out to some kind of help?')
        }
        widgets = {
            'feelings_due_to_lockdown': RadioSelect(),
            'therapist': RadioSelect(),
        }