from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Course, CourseSection, Episode
from .general_courses_serializers import CommentSerializer
from users.serializers.user_serializers import UserSerializer


class EpisodePaidSerializer(ModelSerializer):
    length = serializers.CharField(source="get_video_length_time")
    file = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = Episode
        fields = [
            "title",
            "file",
            "length",
        ]


class CourseSectionPaidSerializer(ModelSerializer):
    episodes = EpisodePaidSerializer(many=True)
    total_duduration = serializers.CharField(source="total_length")

    class Meta:
        model = CourseSection
        fields = [
            "section_title",
            "section_number",
        ]


class CoursePaidSerializer(ModelSerializer):
    comment = CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionPaidSerializer(many=True)
    student_rating = serializers.IntegerField(source="get_rating")
    student_rating_no = serializers.IntegerField(source="get_no_rating")
    student_no = serializers.IntegerField(source="get_enrolled_students")
    total_lectures = serializers.IntegerField(source="get_total_lectures")
    total_duration = serializers.CharField(source="total_course_length")

    class Meta:
        model = Course
        exclude = [
            "rating",
        ]
