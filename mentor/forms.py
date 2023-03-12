from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from quiz.models import Student, Exam


class ExamForm(forms.ModelForm):
    students = ((i+1, str(perm)) for i, perm in enumerate(Student.objects.all()))

    users = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all()
        ,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Exam
        fields = ["name", "duration", "passing_percentage", "users", "active", "show_result",]
        labels = {
            "duration": "Время",
            "name": "Название Теста",
            "passing_percentage": "Проходной процент",
            "active": "Активный?",
            "show_result": "Показать результат"
        }