from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator

ALPHABETS_REGEX = r'^[a-zA-Z][a-zA-Z 1-9:]+$'
QUESTION_REGEX = r'^[a-zA-Z][a-zA-Z 1-9:?!]+$'


# Create your models here.
class Course(models.Model):
    # Course Name
    name = models.CharField(
        verbose_name="Course Name",
        max_length=255,
        blank=False,
        validators=[
            RegexValidator(
                ALPHABETS_REGEX,
                message="Invalid Course Name, Can't Be Empty or Whitespace")
        ])

    # Course Code
    code = models.CharField(
        verbose_name="Course Code",
        max_length=10,
        validators=[MaxLengthValidator(10, "Too Long Course Code")])

    # Course Details
    details = models.TextField(
        verbose_name="Course Details", max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):

    # Chapter Name
    name = models.CharField(
        verbose_name="Chapter Name",
        max_length=255,
        blank=False,
        validators=[
            RegexValidator(
                ALPHABETS_REGEX,
                message="Invalid Chapter Name, Can't Be Empty or Whitespace")
        ])
    # Chapter Details
    details = models.TextField(
        verbose_name="Chapter Details", max_length=512, blank=True, null=True)

    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    OBJECTIVES_CHOICES = (('REMINDING', 'Reminding Question'),
                          ('UNDERSTANDING', 'Measure Understanding'),
                          ('CREATIVITY', 'Measure Creativity'))
    DIFFICULTY_CHOICES = (('DIFFICULT', 'Difficult Question'),
                          ('EASY', 'Easy Question'))
    # Question Content
    content = models.CharField(
        verbose_name="Question",
        max_length=255,
        blank=False,
        validators=[
            RegexValidator(
                QUESTION_REGEX,
                message="Invalid Question Content, Can't Be Empty or Whitespace"
            )
        ])
    # Question Objective
    objective = models.CharField(
        verbose_name="Objective of Question",
        max_length=15,
        choices=OBJECTIVES_CHOICES,
        default='REMINDING')
    # Question Difficulty
    difficulty = models.CharField(
        verbose_name="Difficulty of Question",
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default='EASY')
    # Question Score
    score = models.IntegerField(verbose_name="Question Score")
    #Related Chapter
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Choice(models.Model):
    content = models.CharField(
        verbose_name="Choice",
        max_length=255,
        blank=False,
        validators=[
            RegexValidator(
                ALPHABETS_REGEX,
                message="Invalid Choice Can't Be Empty or Whitespace")
        ])

    # is the right choice?
    is_right = models.BooleanField(
        verbose_name="Is the right choice", default=False)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


# class StudentsExam(models.Model):
#     EXAM_STATE_CHOICES = (('F', 'FAIL'), ('S', 'success'), ('N',
#                                                             'Not Done Yet'))

#     # State Of Exam
#     state = models.CharField(
#         verbose_name="State of Exam",
#         max_length=1,
#         choices=EXAM_STATE_CHOICES,
#         default='N')

#     # name = models.ForeignKeyField('Identity', related_name='student', on_delete=models.CASCADE)