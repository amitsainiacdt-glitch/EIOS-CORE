"""Discover bounded official document assets linked from an approved HTML page."""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit

from modules.external_intelligence.http_retriever import RetrievedContent


_ALLOWED_EXTENSIONS = ('.pdf', '.png', '.jpg', '.jpeg', '.webp')


@dataclass(frozen=True)
class OfficialLinkedAsset:
    url: str
    parent_url: str
    asset_type: str
    relevance_terms: tuple[str, ...]


class _AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag, attrs) -> None:
        values = dict(attrs)
        target = values.get('href') if tag.casefold() == 'a' else values.get('src') if tag.casefold() == 'img' else None
        if target:
            self.targets.append(target)


def discover_official_linked_assets(
    retrieved: RetrievedContent,
    *,
    approved_domain: str,
    relevance_terms: tuple[str, ...],
    max_assets: int = 8,
) -> list[OfficialLinkedAsset]:
    """Return relevant document/image URLs without retrieving or interpreting them."""
    if not isinstance(retrieved, RetrievedContent):
        raise ValueError('retrieved must be RetrievedContent')
    if 'html' not in retrieved.content_type.casefold():
        return []
    domain = approved_domain.strip().casefold().rstrip('.')
    if not domain or urlsplit(retrieved.url).hostname.casefold() != domain:
        raise ValueError('parent page must use the exact approved domain')
    if type(max_assets) is not int or not 1 <= max_assets <= 20:
        raise ValueError('max_assets must be between 1 and 20')
    terms = tuple(dict.fromkeys(term.strip().casefold() for term in relevance_terms if term.strip()))
    if not terms:
        raise ValueError('at least one relevance term is required')

    parser = _AssetParser(); parser.feed(retrieved.content); parser.close()
    candidates = []
    for position, target in enumerate(parser.targets):
        joined = urljoin(retrieved.url, target)
        parts = urlsplit(joined)
        path = parts.path.casefold()
        if parts.scheme != 'https' or (parts.hostname or '').casefold().rstrip('.') != domain:
            continue
        extension = next((item for item in _ALLOWED_EXTENSIONS if path.endswith(item)), None)
        if extension is None:
            continue
        normalized = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ''))
        haystack = normalized.casefold()
        matched = tuple(term for term in terms if term in haystack)
        if not matched:
            continue
        candidates.append((-len(matched), position, normalized, extension, matched))

    result, seen = [], set()
    for _, _, url, extension, matched in sorted(candidates):
        if url in seen:
            continue
        seen.add(url)
        result.append(OfficialLinkedAsset(url, retrieved.url, 'PDF' if extension == '.pdf' else 'IMAGE', matched))
        if len(result) == max_assets:
            break
    return result


__all__ = ['OfficialLinkedAsset', 'discover_official_linked_assets']
