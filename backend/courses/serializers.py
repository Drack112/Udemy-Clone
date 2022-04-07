from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Course
from users.serializers import UserSerializer


class CourseDisplaySerializer(ModelSerializer):
    rating = serializers.IntegerField(source="get_rating")
    student_no = serializers.IntegerField(source="get_enrolled_student")
    author = UserSerializer()

    class Meta:
        model = Course
        fields = [
            "course_uuid",
            "title",
            "rating",
            "student_no",
            "author",
            "price",
            "image_url",
        ]
