# Generated by Django 4.0.3 on 2022-04-07 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="paid_course",
            field=models.ManyToManyField(blank=True, to="courses.course"),
        ),
    ]