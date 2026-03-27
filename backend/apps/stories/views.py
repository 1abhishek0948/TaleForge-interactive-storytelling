from django.conf import settings
from django.db import OperationalError, ProgrammingError
from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Choice, Story, StoryNode, UserProgress
from .permissions import StoryOwnershipPermission, is_story_manager
from .serializers import (
    ChoiceSerializer,
    StoryNodeSerializer,
    StorySerializer,
    UserProgressSerializer,
    UserSerializer,
    UserSignupSerializer,
)
from .services import generate_ai_node
from .demo_users import ensure_demo_login_users


class SignupView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            raise ValidationError({"refresh": "Refresh token is required."})

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            raise ValidationError({"refresh": str(exc)}) from exc
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class ScopedTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        if getattr(settings, "ENABLE_DEMO_LOGIN_USERS", False):
            try:
                ensure_demo_login_users()
            except (OperationalError, ProgrammingError):
                # Keep login endpoint responsive during early startup/migration windows.
                pass
        return super().post(request, *args, **kwargs)


class ScopedTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class TranslationRateThrottle(ScopedRateThrottle):
    scope = "translation"


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _can_manage_story(self, user, story):
        return user.is_authenticated and (story.creator_id == user.id or is_story_manager(user))

    def get_queryset(self):
        queryset = Story.objects.select_related("creator", "starting_node")
        user = self.request.user
        if user.is_authenticated:
            if is_story_manager(user):
                return queryset
            return queryset.filter(Q(is_published=True) | Q(creator=user)).distinct()
        return queryset.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        story = self.get_object()
        if not self._can_manage_story(self.request.user, story):
            raise PermissionDenied("Only the creator, moderator, or admin can edit this story.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self._can_manage_story(self.request.user, instance):
            raise PermissionDenied("Only the creator, moderator, or admin can delete this story.")
        instance.delete()

    def _enforce_story_access(self, story):
        if story.is_published:
            return
        user = self.request.user
        if not self._can_manage_story(user, story):
            raise PermissionDenied("You do not have access to this story.")

    def _build_reader_payload(self, story, node, completed=False, progress=None):
        node_data = StoryNodeSerializer(node).data if node else None
        progress_data = UserProgressSerializer(progress).data if progress else None
        return {
            "story": StorySerializer(story).data,
            "node": node_data,
            "completed": completed,
            "progress": progress_data,
        }

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def read(self, request, pk=None):
        story = self.get_object()
        self._enforce_story_access(story)

        progress = None
        if request.user.is_authenticated:
            progress = UserProgress.objects.filter(user=request.user, story=story).first()

        node = None
        completed = False
        if progress:
            node = progress.current_node
            completed = progress.completed
        elif story.starting_node:
            node = story.starting_node

        return Response(self._build_reader_payload(story, node, completed, progress))

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def start(self, request, pk=None):
        story = self.get_object()
        self._enforce_story_access(story)

        if not story.starting_node:
            raise ValidationError({"starting_node": "Story has no starting node configured."})

        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            story=story,
            defaults={
                "current_node": story.starting_node,
                "path": [story.starting_node.node_key],
                "completed": False,
            },
        )

        progress.current_node = story.starting_node
        progress.path = [story.starting_node.node_key]
        progress.completed = False
        progress.save(update_fields=["current_node", "path", "completed", "updated_at"])

        return Response(self._build_reader_payload(story, progress.current_node, progress.completed, progress))

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def choose(self, request, pk=None):
        story = self.get_object()
        self._enforce_story_access(story)

        if not story.starting_node:
            raise ValidationError({"starting_node": "Story has no starting node configured."})

        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            story=story,
            defaults={
                "current_node": story.starting_node,
                "path": [story.starting_node.node_key],
                "completed": False,
            },
        )

        if progress.completed:
            raise ValidationError({"detail": "Story is already completed. Use /start/ to restart."})

        if not progress.current_node:
            raise ValidationError({"detail": "Progress has no current node. Use /start/ first."})

        choice_id = request.data.get("choice_id")
        if not choice_id:
            raise ValidationError({"choice_id": "choice_id is required."})

        choice = Choice.objects.filter(id=choice_id, node=progress.current_node).first()
        if not choice:
            raise ValidationError({"choice_id": "Choice does not exist for the current node."})

        next_node = generate_ai_node(story, progress.current_node, choice) if choice.requires_ai_generation else choice.next_node

        if next_node is None:
            progress.current_node = None
            progress.completed = True
            progress.path = [*progress.path, "END"]
        else:
            progress.current_node = next_node
            progress.completed = next_node.is_ending
            progress.path = [*progress.path, next_node.node_key]

        progress.save(update_fields=["current_node", "completed", "path", "updated_at"])

        return Response(self._build_reader_payload(story, progress.current_node, progress.completed, progress))

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def progress(self, request, pk=None):
        story = self.get_object()
        progress = UserProgress.objects.filter(user=request.user, story=story).first()
        if not progress:
            return Response({"detail": "No progress yet."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProgressSerializer(progress).data)

    @action(detail=True, methods=["post"], permission_classes=[AllowAny], throttle_classes=[TranslationRateThrottle])
    def translate(self, request, pk=None):
        from .services import (
            TranslationUnavailableError,
            build_translatable_story_payload,
            translate_story_payload,
        )

        story = self.get_object()
        self._enforce_story_access(story)

        target_language = (request.data.get("target_language") or "").strip().lower()
        if not target_language:
            raise ValidationError({"target_language": "target_language is required."})

        if target_language == "original":
            node_id = request.data.get("node_id")
            try:
                payload = build_translatable_story_payload(story, node_id=node_id)
            except ValueError as exc:
                raise ValidationError({"node_id": str(exc)}) from exc
            return Response(
                {
                    "story_title": payload.get("story_title", ""),
                    "story_description": payload.get("story_description", ""),
                    "node_title": payload.get("node_title", ""),
                    "node_content": payload.get("node_content", ""),
                    "choices": [
                        {"id": choice_id, "text": text}
                        for choice_id, text in zip(payload.get("choice_ids", []), payload.get("choice_texts", []))
                    ],
                }
            )

        allowed_languages = set(getattr(settings, "SUPPORTED_TRANSLATION_LANGUAGES", ["en", "hi"]))
        if target_language not in allowed_languages:
            raise ValidationError(
                {"target_language": f"Unsupported language. Allowed: {', '.join(sorted(allowed_languages))}"}
            )

        node_id = request.data.get("node_id")
        try:
            payload = build_translatable_story_payload(story, node_id=node_id)
        except ValueError as exc:
            raise ValidationError({"node_id": str(exc)}) from exc
        try:
            translated = translate_story_payload(payload, target_language=target_language)
        except TranslationUnavailableError as exc:
            raise ValidationError({"detail": str(exc)}) from exc

        return Response(translated)


class StoryNodeViewSet(viewsets.ModelViewSet):
    serializer_class = StoryNodeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StoryOwnershipPermission]

    def get_queryset(self):
        queryset = StoryNode.objects.select_related("story", "story__creator")
        user = self.request.user
        if user.is_authenticated:
            if not is_story_manager(user):
                queryset = queryset.filter(Q(story__is_published=True) | Q(story__creator=user)).distinct()
        else:
            queryset = queryset.filter(story__is_published=True)

        story_id = self.request.query_params.get("story")
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    def _ensure_story_owner(self, story):
        if story.creator_id != self.request.user.id and not is_story_manager(self.request.user):
            raise PermissionDenied("Only the story creator, moderator, or admin can modify nodes.")

    def perform_create(self, serializer):
        story = serializer.validated_data["story"]
        self._ensure_story_owner(story)
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_story_owner(self.get_object().story)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_story_owner(instance.story)
        instance.delete()


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, StoryOwnershipPermission]

    def get_queryset(self):
        queryset = Choice.objects.select_related("node", "node__story", "node__story__creator", "next_node")
        user = self.request.user
        if user.is_authenticated:
            if not is_story_manager(user):
                queryset = queryset.filter(Q(node__story__is_published=True) | Q(node__story__creator=user)).distinct()
        else:
            queryset = queryset.filter(node__story__is_published=True)

        story_id = self.request.query_params.get("story")
        if story_id:
            queryset = queryset.filter(node__story_id=story_id)

        node_id = self.request.query_params.get("node")
        if node_id:
            queryset = queryset.filter(node_id=node_id)

        return queryset

    def _ensure_story_owner(self, story):
        if story.creator_id != self.request.user.id and not is_story_manager(self.request.user):
            raise PermissionDenied("Only the story creator, moderator, or admin can modify choices.")

    def perform_create(self, serializer):
        node = serializer.validated_data["node"]
        self._ensure_story_owner(node.story)
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_story_owner(self.get_object().node.story)
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_story_owner(instance.node.story)
        instance.delete()


class UserProgressViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related("story", "current_node")
