from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
import random
from user.models import User

# Create your models here.
A = "A"
B = "B"
C = "C"
D = "D"

ANSWER_CHOICES = [
    (A, A),
    (B, B),
    (C, C),
    (D, D),
]

def validate_max_duration(value):
    if value > timedelta(hours=23, minutes=59, seconds=59):
        raise ValidationError(
            "Maximum duration is 23 hours, 59 minutes and 59 seconds."
        )


def validate_min_duration(value):
    if value < timedelta(seconds=1):
        raise ValidationError("Minimum duration is 1 second.")

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} | {self.user.first_name} {self.user.last_name}"
class Exam(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(Student, blank=True)
    name = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(
        default=timedelta(hours=1),
        help_text="In format hh:mm:ss",
        validators=[validate_max_duration, validate_min_duration],
    )
    passing_percentage = models.FloatField(default=0)
    active = models.BooleanField()
    show_result = models.BooleanField()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name

class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField(max_length=1000)
    option_A = models.CharField(max_length=200)
    option_B = models.CharField(max_length=200)
    option_C = models.CharField(max_length=200)
    option_D = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default=A)
    marks_on_correct_answer = models.FloatField(default=1)
    marks_on_wrong_answer = models.FloatField(default=0)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.question

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(Question)
    created = models.DateTimeField(auto_now_add=True)
    submitted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created",)

    def get_questions(self):
        questions = list(self.exam.question_set.filter(created__lt=self.created))
        questions = [q for q in questions if not q.deleted or q.deleted > self.created]
        rand = random.Random(self.seed)
        rand.shuffle(questions)

        return questions


    def __str__(self):
        return self.exam.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default=A)

    def get_answer_status(self):
        return self.answer == self.question.correct_answer

    def get_marks(self):
        if self.get_answer_status():
            return self.question.marks_on_correct_answer
        return self.question.marks_on_wrong_answer

    def __str__(self):
        return self.answer