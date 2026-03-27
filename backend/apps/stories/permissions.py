from rest_framework import permissions

from .models import Choice, Story, StoryNode


def is_story_manager(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=["Moderators", "Admins"]).exists()


class StoryOwnershipPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Story):
            story = obj
        elif isinstance(obj, StoryNode):
            story = obj.story
        elif isinstance(obj, Choice):
            story = obj.node.story
        else:
            return False

        if request.method in permissions.SAFE_METHODS:
            return story.is_published or (
                request.user.is_authenticated
                and (story.creator_id == request.user.id or is_story_manager(request.user))
            )

        return request.user.is_authenticated and (
            story.creator_id == request.user.id or is_story_manager(request.user)
        )
