import csv
import os

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, request
from django.forms import ModelForm
from django import forms
from .models import CourseContent, Prof, Spec
from .forms import CourseForm

# Create your views here.

def course_search_form(request):

    submitbutton = request.GET.get("submit")

    semester = ''
    section = ''
    course_credit = ''
    modality = ''

    form = CourseForm(request.GET)
    if form.is_valid():

        semester = form.cleaned_data.get("semester")
        section = form.cleaned_data.get("section")
        course_credit = form.cleaned_data.get("course_credit")
        modality = form.cleaned_data.get("modality")

    context = {'form': form, 'semester': semester, 'section': section, 'modality': modality,
               'submitbutton': submitbutton, 'course_credit': course_credit}

    return render(request, 'home.html', context)


class SearchResultsCourses(ListView):
    model = CourseContent
    template_name = 'display_course_results.html'

    def get_queryset(self):
        semester = self.request.GET.get('semester')
        section = self.request.GET.get('section')
        course_credit = self.request.GET.get('course_credit')
        modality = self.request.GET.get('modality')

        courses = CourseContent.objects.all().filter(
            semester=semester,
            section=section,
            course_credits=course_credit,
            modality=modality
        )

        return courses

class HomePage(ListView):
    model = CourseContent
    template_name = 'home.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('semester')
    #     print(query)
    #     return query

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.import_profs()
        self.import_courses()

    def import_profs(self):

        with open(self.dir_path + '/professors_tab.tsv', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="\t")
            # Professor	Description	Specializations	FOMO

            for i, row in enumerate(reader):
                if i == 0:
                    continue

                if not row:
                    continue
                if not row[0]:
                    continue
                remove_nulls = str(row[0]).replace(" ", "")
                if not remove_nulls:
                    row[0] = "--"

                try:
                    x = Prof.objects.get(prof=row[0])
                    # create the new spec
                    s = None
                    try:
                        s = Spec.objects.get(special=row[2])
                    except:
                        s = Spec(special=row[2], FOMO=row[3])
                    # If created - Save spec before adding new item to it
                    s.save()
                    s.professor.add(x)

                except:
                    # Create new prof
                    x = Prof()
                    x.prof = row[0]
                    x.description = row[1]
                    x.save()
                    # Create the new spec
                    s = None
                    try:
                        s = Spec.objects.get(special=row[2])
                    except:
                        s = Spec(special=row[2], FOMO=row[3])
                    s.save()
                    s.professor.add(x)

    def import_courses(self):
        with open(self.dir_path + '/course_list_tab.tsv', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="\t")
            # Number,Title,Faculty,Semester,Section,Credits,Modality**

            for i, row in enumerate(reader):

                if i == 0:
                    continue
                if not row[2]:
                    continue

                x = CourseContent()
                x.ID = row[0]
                x.title = row[1]
                x.semester = row[3]
                x.section = row[4]
                x.course_credits = row[5]
                x.modality = row[6]
                x.save()
                if ";" in row[2]:
                    profs = str(row[2]).split(";")

                    for item in profs:
                        item_stripped = str(item).strip()
                        if not item:
                            continue

                        try:
                            p = Prof.objects.get(prof=item_stripped)
                            p.courses = x
                            p.save()
                            x.faculty.add(p)
                            x.save()
                        except:
                            p = Prof(prof=item_stripped, description="Not found.")
                            p.save()
                            s = None
                            try:
                                s = Spec.objects.get(special="Unknown")
                            except:
                                s = Spec(special="Unknown", FOMO="N/A")
                            s.save()
                            s.professor.add(p)
                            x.faculty.add(p)
                            x.save()

                else:

                    try:
                        p = Prof.objects.get(prof=row[2])
                        p.courses = x
                        p.save()
                        x.faculty.add(p)
                        x.save()
                    except:
                        p = Prof(prof=row[2], description="Not found.")
                        p.save()
                        s = None
                        try:
                            s = Spec.objects.get(special="Unknown")
                        except:
                            s = Spec(special="Unknown", FOMO="N/A")
                        s.save()
                        s.professor.add(p)
                        x.faculty.add(p)
                        x.save()


class AllCourses(ListView):
    model = CourseContent
    template_name = 'list_courses.html'
    context_object_name = 'course_list'


class AllProfs(ListView):
    model = Prof
    template_name = 'list_profs.html'
    context_object_name = 'prof_list'


class CourseDetails(DetailView):
    model = CourseContent
    template_name = 'course.html'


class ProfDetails(DetailView):
    model = Prof
    template_name = 'profs.html'


