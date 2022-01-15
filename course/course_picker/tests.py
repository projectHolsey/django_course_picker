import csv
import os

from django.test import TestCase
from django.urls import reverse
from .models import Prof, Spec, CourseContent


class split_teacher:
    first_name = ""
    last_name = ""

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CP_Tests(TestCase):

    def setUp(self):
        self.specs = []
        self.lecturers = []
        self.courses = []
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        # self.import_specs()
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
                        try:
                            p = Prof.objects.get(prof=item)
                            p.courses = x
                            p.save()
                            x.faculty.add(p)
                            x.save()
                        except:
                            p = Prof(prof=item, description="Not found.")
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


    def test_contains_professor(self):
        # A019	Education Sector Nonprofits	Honan, James
        # Entry.objects.all()
        for item in CourseContent.objects.all():
            if item.ID == "A019":
                x = item.faculty.all()
                for query in x:
                    # query should be the professor objects
                    # BUT if we just want the str, it should just be the professor name
                    self.assertEqual(str(query), "James P. Honan")

                # print(f"COURSE {item.ID} - {item.title} has a lecturer '{item.faculty.prof}'")
                # self.assertEqual(item.faculty.prof, "James P. Honan")

    def test_contains_2_professors(self):
        for item in CourseContent.objects.all():
            # print("Course id = " + item.ID)
            if item.ID == "A217A":
                # print(item.faculty.all())
                self.assertEqual(len(item.faculty.all()), 2)

    def test_specs_reverse_lookup(self):
        for item in Prof.objects.all():
            if item.prof == "James P. Honan":
                x = item.spec_set.all()
                print("length of queryset is " + str(len(x)))
                # print(x)
                self.assertEqual(len(x), 4)


    def test_contains_professor(self):
        # A019	Education Sector Nonprofits	Honan, James
        # Entry.objects.all()
        for item in CourseContent.objects.all():
            if item.ID == "T581":
                x = item.faculty.all()
                for query in x:
                    # query should be the professor objects
                    # BUT if we just want the str, it should just be the professor name
                    print("She's here...")
                    self.assertEqual(str(query), "Rosenheck, Louisa")


# def import_profs(self):
    #
    #     with open(self.dir_path + '/professors_tab.tsv', encoding='utf-8') as f:
    #         reader = csv.reader(f, delimiter="\t")
    #         # Professor,Description,Specialization
    #         # Professor	Description	Specializations	FOMO
    #
    #         for i, row in enumerate(reader):
    #
    #             if i == 0:
    #                 continue
    #
    #             if Prof.objects.filter(prof = row[0]):
    #                 x = Prof.objects.filter(prof = row[0])
    #                 for i in range(len(x)):
    #                     for item in self.specs:
    #                         if row[2] == item.special:
    #                             # print("Adding specialisation to prof: " + str(item.special))
    #                             x[i].specialisation.add(item)
    #                             #print(f"Adding spec to {x[i].prof} : {item.special}")
    #                             break
    #                     x[i].save()
    #                     spec_list = []
    #                     for item in x[i].specialisation:
    #                         spec_list.append(item)
    #
    #                     #print("prof {0} specialities are {1}".format(x[i].prof, ", ".join(spec_list)))
    #
    #
    #             else:
    #
    #                 x = Prof()
    #                 x.prof = row[0]
    #                 # if "james" in x.prof.lower():
    #                 #     print(x.prof)
    #                 x.description = row[1]
    #
    #                 x.save()
    #
    #         items = Prof.objects.all()
    #         for item in items:
    #             self.lecturers.append(item)

# def import_courses(self):
    #     with open(self.dir_path + '/course_list_tab.tsv', encoding='utf-8') as f:
    #         reader = csv.reader(f, delimiter="\t")
    #         # Number,Title,Faculty,Semester,Section,Credits,Modality**
    #
    #         for i, row in enumerate(reader):
    #
    #             if i == 0:
    #                 continue
    #
    #             members_of_faculty = []
    #
    #             if "various" in str(row[2]).lower():
    #                 faculty = split_teacher()
    #                 faculty.first_name = str(row[2])
    #                 faculty.last_name = str(row[2])
    #                 members_of_faculty.append(faculty)
    #
    #             elif ";" in row[2]:
    #                 x = row[2].split(";")
    #                 # Kim, James; Conaway, Carrie; Bocala Candice; McIntyre, Joseph; Galvez, Sebastian
    #                 # [ "Kim, James", "Conaway, Carrie", "Bocala Candice", "McIntyre, Joseph", "Galvez, Sebastian" ]
    #                 for item in x:
    #                     faculty = split_teacher()
    #                     if not item:
    #                         continue
    #                     item = item.replace(",", "").split(" ")
    #                     if len(item) > 2:
    #                         faculty.first_name = f"{item[1]} {item[2]}"
    #                     else:
    #                         try:
    #                             faculty.first_name = item[1]
    #                         except:
    #                             print("Failed with " + str(item))
    #                     faculty.last_name = item[0]
    #                     members_of_faculty.append(faculty)
    #             else:
    #                 faculty = split_teacher()
    #                 item = str(row[2])
    #                 if not item:
    #                     continue
    #                 item = item.replace(",", "").split(" ")
    #                 if len(item) > 2:
    #                     faculty.first_name = f"{item[1]} {item[2]}"
    #                 else:
    #                     try:
    #                         faculty.first_name = item[1]
    #                     except:
    #                         print("Failed with " + str(item))
    #                 faculty.last_name = item[0]
    #                 members_of_faculty.append(faculty)
    #
    #             # if members_of_faculty:
    #             #     for item in members_of_faculty:
    #             #         print(f"Course : {row[0]} - {row[1]} has faculty member {item.first_name} {item.last_name}")
    #
    #             found_lecturers = []
    #
    #             found = False
    #             for item in self.lecturers:
    #                 for faculty in members_of_faculty:
    #                     if faculty.first_name.lower() in item.prof.lower() or item.prof.lower() in faculty.first_name.lower():
    #                         if faculty.last_name.lower() in item.prof.lower() or item.prof.lower() in faculty.last_name.lower():
    #                             found_lecturers.append(item)
    #                             # print("Found faculty member object in course - " + item.prof)
    #                             found = True
    #             if not found:
    #                 faculty = None
    #
    #             x = CourseContent()
    #
    #             # if found_lecturers:
    #             #     names = []
    #             #     for item in found_lecturers:
    #             #         names.append(item.prof)
    #             #     print(":".join(names))
    #
    #             x.ID = row[0]
    #             x.title = row[1]
    #             # x.faculty =
    #             if found_lecturers:
    #                 for item in found_lecturers:
    #                     print("Faculty before : " + str(x.faculty))
    #                     x.faculty = item
    #                     print("Faculty after : " + str(x.faculty))
    #                 # x.faculty = found_lecturers
    #                 # x.faculty = found_lecturers
    #             else:
    #                 x.faculty = None
    #             x.semester = row[3]
    #             x.section = row[4]
    #             x.course_credits = row[5]
    #             x.modality = row[6]
    #             x.save()
    #             self.courses.append(x)