from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Story(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stories",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    starting_node = models.ForeignKey(
        "StoryNode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        if self.starting_node and self.starting_node.story_id != self.id:
            raise ValidationError("Starting node must belong to the same story.")

    def __str__(self) -> str:
        return self.title


class StoryNode(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="nodes")
    node_key = models.CharField(max_length=100)
    title = models.CharField(max_length=120, blank=True)
    content = models.TextField()
    is_ending = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        unique_together = ("story", "node_key")

    def __str__(self) -> str:
        return f"{self.story.title}::{self.node_key}"


class Choice(models.Model):
    node = models.ForeignKey(StoryNode, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    next_node = models.ForeignKey(
        StoryNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_choices",
    )
    order = models.PositiveIntegerField(default=0)
    requires_ai_generation = models.BooleanField(default=False)
    ai_instruction = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]

    def clean(self) -> None:
        if self.next_node and self.next_node.story_id != self.node.story_id:
            raise ValidationError("Choice next node must belong to the same story.")

    def __str__(self) -> str:
        return f"Choice from {self.node.node_key}"


class UserProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="story_progress",
    )
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="progress_entries")
    current_node = models.ForeignKey(StoryNode, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    path = models.JSONField(default=list, blank=True)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.story.title}"
