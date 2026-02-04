from django.db import models
from django.conf import settings

# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Grade 10"
    section = models.CharField(max_length=10) # e.g., "A"

    def __str__(self):
        return f"{self.name} - {self.section}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.user.username
    
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date') # Prevents double attendance for the same day

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.user.username} - {self.date} ({status})"