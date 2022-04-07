from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
from .models import Sector
from .serializers import CourseDisplaySerializer


class CoursesHomeViews(APIView):
    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by("?")[:6]
        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_courses.order_by("?")[:4]
            courses_serializer = CourseDisplaySerializer(sector_courses, many=True)
            sector_obj = {
                "sector_name": sector.name,
                "sector_uuid": sector.sector_uuid,
                "featured_courses": courses_serializer.data,
                "sector_image": sector.sector_images.url,
            }
            sector_response.append(sector_obj)
            # serializer=SectorSerializer(sectors=sector_response,many=True)

        return Response(data=sector_response, status=status.HTTP_200_OK)
