from django.db import models
from django.contrib.auth.models import User
from adminapp.models import StudentList
class AddCourse(models.Model):
        COURSE_CHOICES = [
            ('AOOP','ADVANCED Object-Oriented Programming'),
            ('PFSD','Python Full Stack Development'),
            ('DBMS','Database Management System'),
            ('LAA','Linux Administration'),
        ]
        SECTION_CHOICES = [
            ('S11', 'Section-11'),
            ('S12', 'Section-12'),
            ('S13', 'Section-13'),
            ('S14', 'Section-14'),
            ('S15', 'Section-15'),
        ]
        student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
        course = models.CharField(max_length=50, choices=COURSE_CHOICES)
        section = models.CharField(max_length=50, choices=SECTION_CHOICES)
        def str(self):
            return f'{self.student.Register_Number} {self.course} ({self.section})'
class Marks(models.Model):
    COURSE_CHOICES=[
        ('AOOP', 'Advanced Object-Oriented Programming'),
        ('PFSD', 'Python Full Stack Development'),
    ]
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    course = models.CharField(max_length=50,choices=COURSE_CHOICES)
    Marks = models.IntegerField()
    def __str__(self):
        return f"{self.student.name} - {self.course}"