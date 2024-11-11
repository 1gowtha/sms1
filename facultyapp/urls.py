from django.urls import path, include
from . import views
app_name='facultyapp'
urlpatterns=[
    path('FacultyHomePage/', views.FacultyHomePage, name='FacultyHomePage'),
    path('add_course/', views.add_course, name='add_course'),
    path('StudentList/', views.view_student_list, name='list'),
    path('post_marks/', views.post_marks, name='post_marks'),

]