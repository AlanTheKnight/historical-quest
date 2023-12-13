# Generated by Django 4.2.8 on 2023-12-13 21:57

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_step_quest"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ending",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("condition", models.CharField(max_length=255, verbose_name="Условие")),
                ("cover", imagekit.models.fields.ProcessedImageField(blank=True, upload_to="covers")),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="endings",
                        to="api.quest",
                        verbose_name="Квест",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="option",
            name="points",
            field=models.IntegerField(default=0, verbose_name="Очки"),
        ),
        migrations.DeleteModel(
            name="CompletedStats",
        ),
    ]
