from __future__ import annotations

import json
import ssl
from typing import Optional
import uuid
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

from .models import Choice, Story, StoryNode

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

try:
    import certifi
except Exception:  # pragma: no cover
    certifi = None

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


class TranslationUnavailableError(Exception):
    pass


def _extract_text(response) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text.strip()

    output = getattr(response, "output", [])
    lines = []
    for item in output:
        for content in getattr(item, "content", []):
            text = getattr(content, "text", None)
            if text:
                lines.append(text)
    return "\n".join(lines).strip()


def _extract_json_array(raw_text: str, expected_len: int) -> list[str]:
    try:
        data = json.loads(raw_text)
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    cleaned = [item if isinstance(item, str) else "" for item in data]
    if len(cleaned) != expected_len:
        return []
    return cleaned


def _translate_with_google_proxy(text: str, target_language: str) -> str:
    params = urlencode(
        {
            "client": "gtx",
            "sl": "auto",
            "tl": target_language,
            "dt": "t",
            "q": text,
        }
    )

    ssl_context = (
        ssl.create_default_context(cafile=certifi.where())
        if certifi is not None
        else ssl.create_default_context()
    )

    with urlopen(f"{GOOGLE_TRANSLATE_URL}?{params}", timeout=10, context=ssl_context) as response:
        payload = response.read().decode("utf-8")

    data = json.loads(payload)
    if not isinstance(data, list) or not data or not isinstance(data[0], list):
        return text

    translated = "".join(
        chunk[0]
        for chunk in data[0]
        if isinstance(chunk, list) and chunk and isinstance(chunk[0], str)
    )
    return translated or text


def translate_texts(texts: list[str], target_language: str) -> list[str]:
    if not texts:
        return []

    if settings.OPENAI_API_KEY and OpenAI is not None:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        numbered = "\n".join([f"{index + 1}. {text}" for index, text in enumerate(texts)])
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Translate each text while preserving meaning and tone. "
                        "Return only a JSON array of strings in the same order."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Target language: {target_language}\n"
                        f"Texts:\n{numbered}\n\n"
                        "Return valid JSON array only."
                    ),
                },
            ],
            max_output_tokens=700,
        )
        raw_output = _extract_text(response)
        parsed = _extract_json_array(raw_output, expected_len=len(texts))
        if parsed:
            return parsed

    if settings.ENABLE_GOOGLE_TRANSLATE_PROXY:
        try:
            return [_translate_with_google_proxy(text, target_language) for text in texts]
        except (URLError, HTTPError, TimeoutError, ssl.SSLError, json.JSONDecodeError) as exc:
            raise TranslationUnavailableError(
                f"Google translation request failed: {exc}. Check server outbound internet/DNS access "
                "and verify translate.googleapis.com is reachable and SSL certificates are valid."
            ) from exc

    raise TranslationUnavailableError(
        "Translation is not configured on this server. "
        "Set OPENAI_API_KEY or ENABLE_GOOGLE_TRANSLATE_PROXY=true."
    )


def build_translatable_story_payload(story: Story, node_id=None) -> dict:
    node = None
    if node_id:
        node = StoryNode.objects.filter(id=node_id, story=story).prefetch_related("choices").first()
        if not node:
            raise ValueError("node_id does not belong to this story.")

    payload = {
        "story_title": story.title,
        "story_description": story.description or "",
        "node_title": "",
        "node_content": "",
        "choice_texts": [],
        "choice_ids": [],
    }

    if node:
        payload["node_title"] = node.title or f"Scene: {node.node_key}"
        payload["node_content"] = node.content or ""
        choices = list(node.choices.all())
        payload["choice_texts"] = [choice.text for choice in choices]
        payload["choice_ids"] = [choice.id for choice in choices]

    return payload


def translate_story_payload(payload: dict, target_language: str) -> dict:
    fields = [
        payload.get("story_title", ""),
        payload.get("story_description", ""),
        payload.get("node_title", ""),
        payload.get("node_content", ""),
        *payload.get("choice_texts", []),
    ]

    translated = translate_texts(fields, target_language=target_language)
    if len(translated) != len(fields):
        # Defensive fallback: keep originals when provider output is malformed.
        translated = fields

    choice_count = len(payload.get("choice_texts", []))
    choice_translations = translated[4 : 4 + choice_count]

    return {
        "story_title": translated[0],
        "story_description": translated[1],
        "node_title": translated[2],
        "node_content": translated[3],
        "choices": [
            {"id": choice_id, "text": text}
            for choice_id, text in zip(payload.get("choice_ids", []), choice_translations)
        ],
    }


def generate_ai_node(story: Story, current_node: StoryNode, choice: Choice) -> Optional[StoryNode]:
    """
    Generates a dynamic story node with OpenAI when configured.
    Falls back to the choice.next_node when API key/client is unavailable.
    """
    if not settings.OPENAI_API_KEY or OpenAI is None:
        return choice.next_node

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = choice.ai_instruction or (
        "Continue this branching story in second person. Keep it concise, vivid, "
        "and end with a cliffhanger suitable for another decision."
    )

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": "You are a narrative engine that writes interactive fiction nodes.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Story title: {story.title}\n"
                        f"Current node: {current_node.node_key}\n"
                        f"Current text: {current_node.content}\n"
                        f"Chosen action: {choice.text}\n"
                        f"Instruction: {prompt}"
                    ),
                },
            ],
            max_output_tokens=220,
        )
        generated_text = _extract_text(response)
    except Exception:
        return choice.next_node

    if not generated_text:
        return choice.next_node

    new_node = StoryNode.objects.create(
        story=story,
        node_key=f"ai-{uuid.uuid4().hex[:10]}",
        title="Generated Scene",
        content=generated_text,
        is_ending=False,
        metadata={"generated": True, "from_choice_id": choice.id},
    )

    if choice.next_node:
        Choice.objects.create(
            node=new_node,
            text="Continue",
            next_node=choice.next_node,
            order=0,
        )
    else:
        new_node.is_ending = True
        new_node.save(update_fields=["is_ending"])

    return new_node
