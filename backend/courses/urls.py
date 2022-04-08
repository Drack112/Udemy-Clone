from django.urls import path

from .views.courses_views import (
    CoursesHomeViews,
    SectorCourse,
    SearchCourse,
    CourseDetail,
)
from .views.users_courses_views import AddComment, CourseStudy, GetCartDetail

urlpatterns = [
    path("", CoursesHomeViews.as_view(), name="courses"),
    path("<uuid:sector_uuid>", SectorCourse.as_view(), name="sector-courses"),
    path("search/<str:search_term>", SearchCourse.as_view(), name="search-courses"),
    path("detail/<uuid:course_uuid>", CourseDetail.as_view(), name="course-detail"),
    path("comment/<uuid:course_uuid>", AddComment.as_view(), name="add-coment"),
    path("study/<uuid:course_uuid>/", CourseStudy.as_view()),
    path("cart/", GetCartDetail.as_view(), name="cart"),
]
