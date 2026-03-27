from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Story",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "creator",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stories", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StoryNode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("node_key", models.CharField(max_length=100)),
                ("title", models.CharField(blank=True, max_length=120)),
                ("content", models.TextField()),
                ("is_ending", models.BooleanField(default=False)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "story",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="nodes", to="stories.story"),
                ),
            ],
            options={
                "ordering": ["id"],
                "unique_together": {("story", "node_key")},
            },
        ),
        migrations.AddField(
            model_name="story",
            name="starting_node",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="stories.storynode"),
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=0)),
                ("requires_ai_generation", models.BooleanField(default=False)),
                ("ai_instruction", models.TextField(blank=True)),
                (
                    "next_node",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="incoming_choices", to="stories.storynode"),
                ),
                (
                    "node",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="choices", to="stories.storynode"),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="UserProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("path", models.JSONField(blank=True, default=list)),
                ("completed", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "current_node",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="stories.storynode"),
                ),
                (
                    "story",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="progress_entries", to="stories.story"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="story_progress", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "unique_together": {("user", "story")},
            },
        ),
    ]
