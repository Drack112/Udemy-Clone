from django.urls import path

from .views import CoursesHomeViews

urlpatterns = [path("", CoursesHomeViews.as_view(), name="courses")]
