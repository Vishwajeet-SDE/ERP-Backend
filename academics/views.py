from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import StudentProfile, Classroom, Attendance, TeacherProfile
from .serializers import StudentListSerializer
from django.db.models import Count, Q

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_by_class(equest, class_id):
    # Get all students belonging to the specific classroom ID
    students = StudentProfile.objects.filter(classroom_id=class_id)
    serializer = StudentListSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_attendance(request):
    class_id = request.data.get('class_id')
    date = request.data.get('date')
    attendance_data = request.data.get('attendance') # Expecting list: [{"id": 1, "status": true}, ...]

    classroom = get_object_or_404(Classroom, id=class_id)

    for record in attendance_data:
        student = get_object_or_404(StudentProfile, id=record['id'])
        # Update if exists, otherwise create
        Attendance.objects.update_or_create(
            student=student,
            date=date,
            defaults={'is_present': record['status'], 'classroom': classroom}
        )

    return Response({"message": "Attendance recorded successfully!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_attendance(request):
    # Ensure the logged-in user has a StudentProfile
    try:
        student_profile = request.user.student_profile
    except AttributeError:
        return Response({"error": "User is not a student"}, status=400)

    # Get all attendance records for this student
    attendance_records = Attendance.objects.filter(student=student_profile)
    
    total_days = attendance_records.count()
    days_present = attendance_records.filter(is_present=True).count()
    
    # Calculate percentage safely
    percentage = (days_present / total_days * 100) if total_days > 0 else 0

    return Response({
        "student_name": request.user.username,
        "total_days": total_days,
        "days_present": days_present,
        "days_absent": total_days - days_present,
        "percentage": round(percentage, 2)
    })