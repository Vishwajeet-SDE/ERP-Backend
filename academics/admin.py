from django.contrib import admin
from .models import Classroom, Subject, StudentProfile, TeacherProfile, Attendance

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'date', 'is_present')
    list_filter = ('classroom', 'date', 'is_present')