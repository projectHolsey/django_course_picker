# from django.contrib import admin
from django.urls import path

from .views import AllCourses, ProfDetails, AllProfs, CourseDetails, HomePage, course_search_form, SearchResultsCourses

urlpatterns = [
    path('', course_search_form, name='search'),
    path('list_courses', AllCourses.as_view(), name='list_courses'),
    path('list_profs', AllProfs.as_view(), name='list_profs'),
    path('prof/<str:pk>/', ProfDetails.as_view(), name='prof_detail'),
    path('prof_detail/<str:pk>/', ProfDetails.as_view(), name='prof_details'),
    path('course/<int:pk>/', CourseDetails.as_view(), name='course_detail'),
    path('course_search/', SearchResultsCourses.as_view(), name='search_results_courses')
]
