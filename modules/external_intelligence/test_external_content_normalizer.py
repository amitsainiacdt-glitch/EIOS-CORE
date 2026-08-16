"""
EIOS
Everest Investment Operating System

External Content Normalizer Test
=================================
"""

from modules.external_intelligence.external_content_normalizer import (
    ExternalContentNormalizer,
    NormalizedExternalContent,
)

from modules.external_intelligence.http_retriever import (
    RetrievedContent,
)


def main() -> None:

    normalizer = ExternalContentNormalizer()

    # ======================================================
    # ENGINE
    # ======================================================

    assert normalizer is not None

    print(
        "External Content Normalizer : PASS"
    )

    # ======================================================
    # HTML NORMALIZATION
    # ======================================================

    html = """
    <html>
        <head>
            <title>Test Page</title>
            <style>
                body { color: red; }
            </style>
            <script>
                alert("ignore");
            </script>
        </head>

        <body>

            <h1>Tata Motors Demand</h1>

            <p>
                Passenger vehicle demand is increasing.
            </p>

            <div>
                <span>Production remains strong.</span>
            </div>

        </body>
    </html>
    """

    retrieved = RetrievedContent(
        url="https://example.com/test",
        status_code=200,
        content=html,
        content_type="text/html; charset=utf-8",
        headers={
            "Content-Type": "text/html; charset=utf-8"
        },
    )

    result = normalizer.normalize(
        retrieved
    )

    assert isinstance(
        result,
        NormalizedExternalContent,
    )

    print(
        "HTML Normalization           : PASS"
    )

    # ======================================================
    # CONTENT PRESERVATION
    # ======================================================

    assert (
        result.original_content
        == html
    )

    assert (
        result.url
        == retrieved.url
    )

    assert (
        result.status_code
        == retrieved.status_code
    )

    assert (
        result.content_type
        == retrieved.content_type
    )

    print(
        "Original Content Preservation: PASS"
    )

    # ======================================================
    # HTML NOISE REMOVAL
    # ======================================================

    assert (
        "alert"
        not in result.normalized_text
    )

    assert (
        "color: red"
        not in result.normalized_text
    )

    assert (
        "Tata Motors Demand"
        in result.normalized_text
    )

    assert (
        "Passenger vehicle demand is increasing."
        in result.normalized_text
    )

    assert (
        "Production remains strong."
        in result.normalized_text
    )

    print(
        "HTML Noise Removal           : PASS"
    )

    # ======================================================
    # WHITESPACE NORMALIZATION
    # ======================================================

    assert (
        "  "
        not in result.normalized_text
    )

    assert (
        "\n"
        not in result.normalized_text
    )

    print(
        "Whitespace Normalization     : PASS"
    )

    # ======================================================
    # PLAIN TEXT
    # ======================================================

    plain = RetrievedContent(
        url="https://example.com/plain",
        status_code=200,
        content=(
            "Tata Motors   demand\n"
            "is increasing.\n\n"
            "Production remains strong."
        ),
        content_type="text/plain",
        headers={
            "Content-Type": "text/plain"
        },
    )

    plain_result = normalizer.normalize(
        plain
    )

    assert (
        plain_result.normalized_text
        == (
            "Tata Motors demand is increasing. "
            "Production remains strong."
        )
    )

    print(
        "Plain Text Normalization     : PASS"
    )

    # ======================================================
    # SEMANTIC CONTENT EXTRACTION
    # ======================================================

    semantic_html = """
    <html>
        <body>

            <header>
                Site Navigation
            </header>

            <main>

                <div class="entry-content">

                    <aside>
                        Login to download
                    </aside>

                    <h2>Summary</h2>

                    <p>
                        Tata Motors demand is improving.
                    </p>

                    <p>
                        New models are supporting growth.
                    </p>

                </div>

            </main>

            <footer>
                Footer Navigation
            </footer>

        </body>
    </html>
    """

    semantic_retrieved = RetrievedContent(
        url="https://example.com/article",
        status_code=200,
        content=semantic_html,
        content_type="text/html",
        headers={
            "Content-Type": "text/html"
        },
    )

    semantic_result = (
        normalizer.normalize(
            semantic_retrieved
        )
    )

    assert (
        "Tata Motors demand is improving."
        in semantic_result.normalized_text
    )

    assert (
        "New models are supporting growth."
        in semantic_result.normalized_text
    )

    assert (
        "Site Navigation"
        not in semantic_result.normalized_text
    )

    assert (
        "Footer Navigation"
        not in semantic_result.normalized_text
    )

    print(
        "Semantic Content Extraction   : PASS"
    )

    # ======================================================
    # INPUT IMMUTABILITY
    # ======================================================

    assert (
        retrieved.content
        == html
    )

    assert (
        retrieved.url
        == "https://example.com/test"
    )

    print(
        "Input Immutability           : PASS"
    )

    # ======================================================
    # NULL PROTECTION
    # ======================================================

    try:

        normalizer.normalize(
            None
        )

        raise AssertionError(
            "None input accepted"
        )

    except ValueError:

        pass

    print(
        "Invalid Input Protection     : PASS"
    )

    # ======================================================
    # NO ANALYTICAL FABRICATION
    # ======================================================

    assert not hasattr(
        result,
        "confidence",
    )

    assert not hasattr(
        result,
        "evidence_score",
    )

    assert not hasattr(
        result,
        "opportunity_score",
    )

    assert not hasattr(
        result,
        "valuation",
    )

    print(
        "Analytical Boundary          : PASS"
    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("---")
    print()

    print(
        "EIOS EXTERNAL CONTENT "
        "NORMALIZER : PASS"
    )


if __name__ == "__main__":
    main()