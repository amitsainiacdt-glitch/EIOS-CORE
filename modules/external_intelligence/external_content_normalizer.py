"""
EIOS
Everest Investment Operating System

External Content Normalizer
===========================

Purpose
-------
Converts retrieved external web content into deterministic,
readable text suitable for downstream research.

Design Principles
-----------------
- Transformation only.
- No search.
- No HTTP retrieval.
- No source-quality assessment.
- No evidence assessment.
- No investment analysis.
- No summarization.
- No scoring.
- Preserves original retrieved content.
- Deterministic output.
- Uses semantic HTML containers when available.
- Falls back safely when semantic containers are unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)


@dataclass(frozen=True)
class NormalizedExternalContent:
    """
    Immutable normalized representation of retrieved content.
    """

    url: str

    status_code: int

    original_content: str

    normalized_text: str

    content_type: str


class _HTMLTextExtractor(HTMLParser):
    """
    Deterministic HTML-to-text extractor.

    The parser can optionally restrict extraction to a selected
    semantic container.

    It performs no semantic interpretation.
    """

    _IGNORED_TAGS = {
        "script",
        "style",
        "noscript",
        "svg",
    }

    _BLOCK_TAGS = {
        "article",
        "aside",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "main",
        "p",
        "section",
        "tr",
    }

    def __init__(
        self,
        target_tag: str | None = None,
        target_class: str | None = None,
    ) -> None:

        super().__init__()

        self.parts: list[str] = []

        self._ignored_depth = 0

        self._target_tag = (
            target_tag.lower()
            if target_tag
            else None
        )

        self._target_class = (
            target_class.lower()
            if target_class
            else None
        )

        self._target_depth = 0

        self._inside_target = (
            self._target_tag is None
            and self._target_class is None
        )

    def _matches_target(
        self,
        tag: str,
        attrs,
    ) -> bool:

        if self._target_tag is not None:
            if tag != self._target_tag:
                return False

        if self._target_class is not None:

            attributes = dict(attrs)

            class_value = (
                attributes.get("class", "")
            )

            classes = {
                value.lower()
                for value in class_value.split()
            }

            if self._target_class not in classes:
                return False

        return True

    def handle_starttag(
        self,
        tag: str,
        attrs,
    ) -> None:

        tag = tag.lower()

        if tag in self._IGNORED_TAGS:

            self._ignored_depth += 1
            return

        if not self._inside_target:

            if self._matches_target(
                tag,
                attrs,
            ):

                self._inside_target = True
                self._target_depth = 1

            return

        if self._target_depth > 0:

            self._target_depth += 1

        if tag in self._BLOCK_TAGS:

            self.parts.append("\n")

    def handle_startendtag(
        self,
        tag: str,
        attrs,
    ) -> None:

        if (
            self._inside_target
            and tag.lower()
            not in self._IGNORED_TAGS
        ):

            self.parts.append("\n")

    def handle_endtag(
        self,
        tag: str,
    ) -> None:

        tag = tag.lower()

        if tag in self._IGNORED_TAGS:

            if self._ignored_depth > 0:
                self._ignored_depth -= 1

            return

        if not self._inside_target:
            return

        if tag in self._BLOCK_TAGS:
            self.parts.append("\n")

        if (
            self._target_tag is not None
            or self._target_class is not None
        ):

            self._target_depth -= 1

            if self._target_depth <= 0:

                self._inside_target = False

    def handle_data(
        self,
        data: str,
    ) -> None:

        if self._ignored_depth > 0:
            return

        if not self._inside_target:
            return

        text = data.strip()

        if text:
            self.parts.append(text)

    def text(self) -> str:

        return " ".join(self.parts)


class ExternalContentNormalizer:
    """
    Deterministically normalizes RetrievedContent.
    """

    def normalize(
        self,
        retrieved: RetrievedContent,
    ) -> NormalizedExternalContent:
        """
        Normalize retrieved external content.

        No analytical transformation is performed.
        """

        if retrieved is None:

            raise ValueError(
                "retrieved must not be None"
            )

        if not isinstance(
            retrieved,
            RetrievedContent,
        ):

            raise ValueError(
                "retrieved must be RetrievedContent"
            )

        normalized_text = (
            self._normalize_content(
                retrieved.content,
                retrieved.content_type,
            )
        )

        return NormalizedExternalContent(
            url=retrieved.url,

            status_code=retrieved.status_code,

            original_content=retrieved.content,

            normalized_text=normalized_text,

            content_type=retrieved.content_type,
        )

    # ======================================================
    # CONTENT NORMALIZATION
    # ======================================================

    def _normalize_content(
        self,
        content: str,
        content_type: str,
    ) -> str:
        """
        Convert retrieved content into readable text.

        HTML content is parsed structurally.

        Non-HTML content is preserved after
        whitespace normalization.
        """

        if not isinstance(
            content,
            str,
        ):

            raise ValueError(
                "content must be a string"
            )

        content_type_lower = (
            content_type.lower()
            if isinstance(
                content_type,
                str,
            )
            else ""
        )

        if "html" in content_type_lower:

            return self._normalize_html(
                content
            )

        return self._normalize_plain_text(
            content
        )

    # ======================================================
    # HTML
    # ======================================================

    def _normalize_html(
        self,
        content: str,
    ) -> str:
        """
        Prefer semantic article content.

        Extraction order:

            entry-content
                ↓
            article
                ↓
            main
                ↓
            complete document
        """

        candidates = [
            (
                "class",
                "entry-content",
            ),
            (
                "tag",
                "article",
            ),
            (
                "tag",
                "main",
            ),
        ]

        for mode, value in candidates:

            if mode == "class":

                parser = _HTMLTextExtractor(
                    target_class=value
                )

            else:

                parser = _HTMLTextExtractor(
                    target_tag=value
                )

            parser.feed(content)
            parser.close()

            extracted = (
                self._collapse_whitespace(
                    parser.text()
                )
            )

            if extracted:

                return extracted

        # --------------------------------------------------
        # FALLBACK
        # --------------------------------------------------

        parser = _HTMLTextExtractor()

        parser.feed(content)
        parser.close()

        return self._collapse_whitespace(
            parser.text()
        )

    # ======================================================
    # PLAIN TEXT
    # ======================================================

    def _normalize_plain_text(
        self,
        content: str,
    ) -> str:

        return self._collapse_whitespace(
            content
        )

    # ======================================================
    # WHITESPACE
    # ======================================================

    def _collapse_whitespace(
        self,
        text: str,
    ) -> str:

        return " ".join(
            text.split()
        )


__all__ = [
    "NormalizedExternalContent",
    "ExternalContentNormalizer",
]