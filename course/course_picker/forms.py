import datetime

from django import forms
from .models import CourseContent
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CourseForm(forms.Form):

    semesters = CourseContent.objects.values_list('semester', flat=True).distinct()
    sections = CourseContent.objects.values_list('section', flat=True).distinct()
    course_credits = CourseContent.objects.values_list('course_credits', flat=True).distinct()
    modalities = CourseContent.objects.values_list('modality', flat=True).distinct()

    semester = forms.ModelMultipleChoiceField(semesters)
    section = forms.ModelMultipleChoiceField(sections)
    course_credit = forms.ModelMultipleChoiceField(course_credits)
    modality = forms.ModelMultipleChoiceField(modalities)
