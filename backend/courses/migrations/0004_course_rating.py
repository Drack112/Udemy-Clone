# Generated by Django 4.0.3 on 2022-04-07 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="rating",
            field=models.ManyToManyField(blank=True, to="courses.rate"),
        ),
    ]