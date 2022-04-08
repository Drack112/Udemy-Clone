import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed

# Create your views here.
from ..models import Course
from ..serializers.general_courses_serializers import (
    CommentSerializer,
    CartItemSerializer,
)
from ..serializers.paid_courses_serializer import CoursePaidSerializer


class AddComment(APIView):
    def post(self, request, course_uuid, *args, **kwargs):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        content = json.loads(request.body)

        if not content.get("message"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=content)

        if serializer.is_valid():
            comment = serializer.save(user=request.user)

            course.comment.add(comment)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCartDetail(APIView):
    def post(self, request):
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()

        if type(body.get("cart")) != list:
            return HttpResponseBadRequest()

        if len(body.get("cart")) == 0:
            return Response([])

        courses = []

        for uuid in body.get("cart"):
            item = Course.objects.filter(course_uuid=uuid)

            if not item:
                return HttpResponseBadRequest()

            courses.append(item[0])

        serializer = CartItemSerializer(courses, many=True)

        car_total = Decimal(0.00)
        for item in serializer.data:
            car_total += Decimal(item.get("price"))

        return Response(
            data={"cart_detail": serializer.data, "cart_total": car_total},
            status=status.HTTP_200_OK,
        )


class CourseStudy(APIView):
    def get(self, request, course_uuid):
        check_course = Course.objects.filter(course_uuid=course_uuid)

        if not check_course:
            return HttpResponseBadRequest("Course does not exist")

        user_course = request.user.paid_course.filter(course_uuid=course_uuid)

        if not user_course:
            return HttpResponseNotAllowed("User has not purchased this course")

        course = Course.objects.filter(course_uuid=course_uuid)[0]

        serializer = CoursePaidSerializer(course)

        return Response(serializer.data, status=status.HTTP_200_OK)
