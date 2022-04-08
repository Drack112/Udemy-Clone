import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal
from mutagen.mp4 import MP4, MP4StreamInfoError

from .helpers.get_timer import get_timer

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sector(Base):
    name = models.CharField(max_length=255, blank=False, null=False)
    sector_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    related_courses = models.ManyToManyField("Course", null=True, blank=True)
    sector_images = models.ImageField(
        upload_to="sector/thumbs", blank=False, null=False
    )

    def get_image_url(self):
        return f"http://localhost:8000{self.get_image_url.url}"

    def __str__(self) -> str:
        return self.name


class Course(Base):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, blank=False, null=False)
    rating = models.ManyToManyField("Rate", blank=True)
    course_section = models.ManyToManyField("CourseSection", blank=False, null=False)
    comments = models.ManyToManyField("Comment", blank=True)
    image_url = models.ImageField(
        upload_to="courses/thumbs_courses", blank=False, null=False
    )
    course_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    def get_image_url(self):
        return f"http://localhost:8000{self.image_url.url}"

    def get_rating(self):
        ratings = self.rating.all()
        rate = 0
        for rating in ratings:
            rate += rating.rate_number
        try:
            rate /= len(ratings)
        except ZeroDivisionError:
            rate = 0

    def get_no_rating(self):
        return len(self.rating.all())

    def get_brief_description(self):
        return self.description[:100]

    def get_enrolled_students(self):
        students = get_user_model().objects.filter(paid_course=self)
        return len(students)

    def get_total_lectures(self):
        lectures = 0
        for section in self.course_section.all():
            lectures += len(section.episodes.all())
            return lectures

    def total_course_length(self):
        length = Decimal(0.00)

        for section in self.course_section.all():
            for episode in section.episodes.all():
                length += episode.lenght

        return get_timer(length, type="short")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self) -> str:
        return self.title


class Rate(Base):
    rate_number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )


class CourseSection(Base):
    section_title = models.CharField(max_length=255, blank=False, null=False)
    episodes = models.ManyToManyField("Episode", blank=False, null=False)

    def total_length(self):
        total = Decimal(0.00)
        for episode in self.episodes.all():
            total += episode.lenght
        return get_timer(total, type="min")

    def __str__(self) -> str:
        return self.section_title


class Episode(Base):
    title = models.CharField(max_length=255, blank=False, null=False)
    file = models.FileField(upload_to="courses/course_videos", blank=False, null=False)
    lenght = models.DecimalField(max_digits=100, decimal_places=2)

    def get_video_length(self):
        try:
            video = MP4(self.file)
            return video.info.length
        except MP4StreamInfoError:
            return 0.0

    def get_url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        self.lenght = self.get_video_length()

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Comment(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self) -> str:
        return self.user.name
