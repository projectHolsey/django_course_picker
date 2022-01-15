import os
import csv

# file_2 = open("course_list2.csv", "x")
#
# dir_path = os.path.dirname(os.path.realpath(__file__))
#
# new_cotent = ""
# with open(dir_path + '/course_list.csv', encoding='utf8') as f:
#     x = f.readlines()
#     for line in x:
#         if "\"" in line:
#             new_line = line.split("\"")
#
#             my_teacher = new_line[1]
#             if ";" in new_line[1]:
#                 print(my_teacher)
#                 teachers = new_line[1].split(";")
#                 end = ""
#                 for c_teacher in teachers:
#                     try:
#                         end += "{1} {0}".format(c_teacher[:c_teacher.index(",")], c_teacher[c_teacher.index(",") + 1:])
#                         end = end.replace("  ", " ")
#                         end += ";"
#                     except:
#                         end += c_teacher
#                 if ";" is end[:-1]:
#                     end = end[:-1]
#             else:
#                 new_line[1] = "{1} {0}".format(my_teacher[:my_teacher.index(",")], my_teacher[my_teacher.index(",") + 1:])
#
#             for item in new_line:
#                 new_cotent += item
#
#
# file_2.write(new_cotent)

class before_after:
    name_before = ""
    name_corrected = ""
    name_after = ""


class split_teacher:
    first_name = ""
    last_name = ""

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

list_of_names_before_after = []
course_list_names = []
professor_names = []
def sort_names(row):

    if ";" in row:
        x = row.split(";")
        # Kim, James; Conaway, Carrie; Bocala Candice; McIntyre, Joseph; Galvez, Sebastian
        # [ "Kim, James", "Conaway, Carrie", "Bocala Candice", "McIntyre, Joseph", "Galvez, Sebastian" ]
        for spl in x:
            faculty = split_teacher()
            if not spl:
                continue

            if "various" in str(row).lower():
                faculty.first_name = str(row)
                faculty.last_name = str(row)
            else:
                item = spl.replace(",", "").split(" ")
                if len(item) > 2:
                    faculty.first_name = f"{item[1]} {item[2]}"
                else:
                    try:
                        faculty.first_name = item[1]
                    except:
                        print("Failed with " + str(item))
                faculty.last_name = item[0]

            x = before_after()
            x.name_before = spl
            x.name_corrected = f"{faculty.first_name} {faculty.last_name}"
            for item2 in professor_names:
                if str(faculty.first_name).lower() in str(item2).lower():
                    if str(faculty.last_name).lower() in str(item2).lower():

                        x.name_after = item2
                        break
            list_of_names_before_after.append(x)

    else:
        faculty = split_teacher()
        if "various" in str(row).lower():

            faculty.first_name = str(row)
            faculty.last_name = str(row)
            x = before_after()
            x.name_before = row
            x.name_corrected = f"{faculty.first_name} {faculty.last_name}"
            for item2 in professor_names:
                if str(faculty.first_name).lower() in str(item2).lower():
                    if str(faculty.last_name).lower() in str(item2).lower():

                        x.name_after = item2
                        break
            list_of_names_before_after.append(x)
        else:
            # Singular entry
            item = str(row)
            if not item:
                return None
            item = item.replace(",", "").split(" ")
            if len(item) > 2:
                faculty.first_name = f"{item[1]} {item[2]}"
            else:
                try:
                    faculty.first_name = item[1]
                except:
                    print("Failed with " + str(item))
            faculty.last_name = item[0]

            x = before_after()
            x.name_before = row
            x.name_corrected = f"{faculty.first_name} {faculty.last_name}"
            for item2 in professor_names:
                if str(faculty.first_name).lower() in str(item2).lower():
                    if str(faculty.last_name).lower() in str(item2).lower():

                        x.name_after = item2
                        break
            list_of_names_before_after.append(x)

dir_path = os.path.dirname(os.path.realpath(__file__))


with open(dir_path + '/course_list_tab.tsv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    # Number,Title,Faculty,Semester,Section,Credits,Modality**

    for i, row in enumerate(reader):
        if i == 0:
            continue
        course_list_names.append(row[2])

with open(dir_path + '/professors_tab.tsv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    # Professor	Description	Specializations	FOMO

    for i, row in enumerate(reader):
        if i == 0:
            continue
        professor_names.append(row[0])

course_list_names_corrected = []
for item in course_list_names:
    # Returns a list of split_teacher objects
    course_list_names_corrected = sort_names(item)

names_printed = []
counter = 1
for item in list_of_names_before_after:
    if item.name_after:
        if item.name_after not in names_printed:
            counter += 1
            names_printed.append(item.name_after)

            print(str(counter) + " find : {0} - Replace : {2}"
                  .format(item.name_before, item.name_corrected, item.name_after))
