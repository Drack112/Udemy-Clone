# Generated by Django 4.0.3 on 2022-04-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_alter_sector_related_courses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="comments",
            field=models.ManyToManyField(blank=True, to="courses.comment"),
        ),
    ]