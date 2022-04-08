from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Course, CourseSection, Episode
from .general_courses_serializers import CommentSerializer

from users.serializers.user_serializers import UserSerializer


class EpisodeUnPaidSerializer(ModelSerializer):
    lenght = serializers.CharField(source="get_video_length")

    class Meta:
        model = Episode
        fields = [
            "title",
            "lenght",
            "id",
        ]


class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes = EpisodeUnPaidSerializer(many=True)
    total_duration = serializers.CharField(source="total_length")

    class Meta:
        model = CourseSection
        fields = ["section_title", "episodes", "total_duration"]


class CourseUnPaidSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    author = UserSerializer()
    course_section = CourseSectionUnPaidSerializer(many=True)
    student_rating = serializers.IntegerField(source="get_rating")
    student_rating_no = serializers.IntegerField(source="get_no_rating")
    student_no = serializers.IntegerField(source="get_enrolled_students")
    total_lectures = serializers.IntegerField(source="get_total_lectures")
    total_duration = serializers.CharField(source="total_course_length")
    image_url = serializers.ImageField(source="get_image_url")

    class Meta:
        model = Course
        exclude = [
            "rating",
        ]
