from django.db import models


# Create your models here.

class CourseContent(models.Model):
    ID = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    faculty = models.ManyToManyField('Prof')
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    course_credits = models.CharField(max_length=50)
    modality = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.ID} - {self.title}"


class Prof(models.Model):
    prof = models.CharField(primary_key=True, blank=False, null=False, max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.prof}"


class Spec(models.Model):
    special = models.CharField(primary_key=True, max_length=100)
    FOMO = models.CharField(max_length=50)

    professor = models.ManyToManyField(Prof)

    def __str__(self):
        return f"{self.FOMO} : {self.special}"



