from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Course, Comment
from users.serializers.user_serializers import UserSerializer


class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "message", "id"]


class CourseDisplaySerializer(ModelSerializer):
    rating = serializers.IntegerField(source="get_rating")
    student_no = serializers.IntegerField(source="get_enrolled_students")
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


class CourseListSerializer(ModelSerializer):
    rating = serializers.IntegerField(source="get_rating")
    student_no = serializers.IntegerField(source="get_enrolled_students")
    author = UserSerializer()
    description = serializers.CharField(source="get_brief_description")
    total_lectures = serializers.IntegerField(source="get_total_lectures")

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
            "description",
            "total_lectures",
        ]


class CartItemSerializer(ModelSerializer):
    author = UserSerializer()
    image_url = serializers.CharField(source="get_image_url")

    class Meta:
        model = Course
        fields = ["author", "title", "price", "image_url"]
