from rest_framework import serializers
from .models import StudentProfile, Classroom
from users.serializers import UserSerializer

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'section']

class StudentListSerializer(serializers.ModelSerializer):
    # We nest the UserSerializer to get the student's name/email
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'roll_number', 'admission_number']