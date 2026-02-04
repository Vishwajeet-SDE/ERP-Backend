from django.urls import path
from academics.views import get_students_by_class, submit_attendance, get_my_attendance

urlpatterns = [
    path('class-students/<int:class_id>/', get_students_by_class, name='class_students'),
    path('submit-attendance/', submit_attendance, name='submit_attendance'),
    path('my-attendance/', get_my_attendance, name='my_attendance'),
]