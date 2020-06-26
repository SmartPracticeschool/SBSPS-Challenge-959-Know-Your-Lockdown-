from django.db import models
from .district import District
Age_Groups = (
    ('18-', 'Below 18 years'),
    ('18-30', '18-30 years'),
    ('30+', 'Above 30 years')
)

Genders = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

Common_Choices = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('maybe', 'Maybe')
)

Common_Choices_2 = (
    ('yes', 'Yes'),
    ('no', 'No')
)

# Create your models here.
class Quiz(models.Model):
    dist = models.CharField(
                            max_length=50,
                            choices=District,
                            default=District
                            )

    age = models.CharField(
                            max_length=30,
                            choices=Age_Groups,
                            default=Age_Groups
                            )

    gender = models.CharField(
                                max_length = 10,
                                choices = Genders,
                                default = Genders)

    negative_effect = models.CharField(
                                max_length = 10,
                                choices = Common_Choices,
                                default = Common_Choices)

    previously_suffered = models.CharField(
                                max_length = 10,
                                choices = Common_Choices,
                                default = Common_Choices)

    currently_experiencing_symptoms = models.CharField(
                                max_length = 10,
                                choices = Common_Choices,
                                default = Common_Choices)

    feelings_due_to_lockdown = models.CharField(
                                max_length = 10,
                                choices = Common_Choices_2[1:],
                                default = 'no')

    therapist = models.CharField(
                                max_length = 10,
                                choices = Common_Choices_2[1:],
                                default = 'no')
