from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Choice, Story, StoryNode, UserProgress

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    node_id = serializers.PrimaryKeyRelatedField(source="node", queryset=StoryNode.objects.all(), write_only=True)
    node = serializers.IntegerField(source="node_id", read_only=True)
    next_node_id = serializers.PrimaryKeyRelatedField(
        source="next_node", queryset=StoryNode.objects.all(), allow_null=True, required=False
    )
    next_node_key = serializers.CharField(source="next_node.node_key", read_only=True)

    class Meta:
        model = Choice
        fields = [
            "id",
            "node_id",
            "node",
            "text",
            "next_node_id",
            "next_node_key",
            "order",
            "requires_ai_generation",
            "ai_instruction",
        ]

    def validate(self, attrs):
        node = attrs.get("node") or getattr(self.instance, "node", None)
        next_node = attrs.get("next_node") if "next_node" in attrs else getattr(self.instance, "next_node", None)

        if node and next_node and node.story_id != next_node.story_id:
            raise serializers.ValidationError("Choice and next node must belong to the same story.")
        return attrs


class StoryNodeSerializer(serializers.ModelSerializer):
    story_id = serializers.PrimaryKeyRelatedField(source="story", queryset=Story.objects.all(), write_only=True)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = StoryNode
        fields = ["id", "story_id", "node_key", "title", "content", "is_ending", "metadata", "choices", "created_at"]


class StorySerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    starting_node_id = serializers.PrimaryKeyRelatedField(
        source="starting_node", queryset=StoryNode.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "description",
            "is_published",
            "creator",
            "starting_node_id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        story = self.instance
        starting_node = attrs.get("starting_node")
        if not story and starting_node:
            raise serializers.ValidationError("Set the starting node after creating the story.")
        if story and starting_node and starting_node.story_id != story.id:
            raise serializers.ValidationError("Starting node must belong to this story.")
        return attrs


class UserProgressSerializer(serializers.ModelSerializer):
    story = StorySerializer(read_only=True)
    current_node = StoryNodeSerializer(read_only=True)

    class Meta:
        model = UserProgress
        fields = ["id", "story", "current_node", "path", "completed", "updated_at"]
