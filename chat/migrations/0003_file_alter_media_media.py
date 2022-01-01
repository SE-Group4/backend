# Generated by Django 4.2 on 2023-04-13 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_links_room_description_room_participants_media"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="uploads/files")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="media",
            name="media",
            field=models.ImageField(upload_to="uploads/images"),
        ),
    ]
