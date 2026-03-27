from django.contrib import admin

from .models import Choice, Story, StoryNode, UserProgress


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "creator", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "description", "creator__username")


@admin.register(StoryNode)
class StoryNodeAdmin(admin.ModelAdmin):
    list_display = ("id", "story", "node_key", "is_ending")
    search_fields = ("story__title", "node_key", "content")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "node", "text", "next_node", "order", "requires_ai_generation")
    list_filter = ("requires_ai_generation",)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "story", "current_node", "completed", "updated_at")
    list_filter = ("completed",)
