"""Offline fail-closed search provider for environments without network access."""
from modules.external_intelligence.search_provider import SearchProvider


class LocalSearchProvider(SearchProvider):
    provider_id = "LOCAL_OFFLINE"

    def search(self, query):
        # Local documents are ingested through the official-document pipeline;
        # this provider never invents search results.
        return []
