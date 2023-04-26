# Generated by Django 4.2 on 2022-01-01 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rooms", "0001_initial"),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rooms.schedule"
            ),
        ),
        migrations.AddField(
            model_name="roommessage",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages_sent",
                to="chat.user",
            ),
        ),
        migrations.AddField(
            model_name="roommessage",
            name="room",
            field=models.ManyToManyField(related_name="messages", to="rooms.room"),
        ),
        migrations.AddField(
            model_name="privatemessage",
            name="recipient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_private_message",
                to="chat.user",
            ),
        ),
        migrations.AddField(
            model_name="privatemessage",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sent_private_message",
                to="chat.user",
            ),
        ),
    ]
