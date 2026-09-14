"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in week 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# The `# Title` on the first line of every document, and the `## Heading` that
# starts each section.
TITLE_LINE = re.compile(r"(?m)\A#[ \t]+(.+?)[ \t]*$")
SECTION_START = re.compile(r"(?m)^(?=##[ \t])")

# A chunk below this is a fragment rather than an answer. The corpus's real
# sections run 176–711 characters, so nothing legitimate is near it.
MIN_CHUNK = 150


def _split_long_section(body: str, limit: int) -> list[str]:
    """Break an oversized section at blank lines, never mid-sentence."""
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

    pieces: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if current and len(candidate) > limit:
            pieces.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        pieces.append(current)

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split each document at its `##` section headings.

    Every document in `city_guides` is already divided into labelled sections —
    Getting there, Eat and drink, When to go — and each one is a self-contained
    answer to a single question. The section is the unit of meaning here, so
    that is what this cuts on. A character count cuts across it for no reason.

    Two things this does that a plain section split would not:

    1. Every chunk carries its document's `# Title`. Nine of the fourteen
       documents contain a section called "Getting there", and on its own that
       text never says which town it is about — Kestrelford's and Halden Bay's
       are indistinguishable once the filename is gone. Repeating the title is
       the context that makes a section stand alone.

    2. Sections shorter than MIN_CHUNK merge into the one before them, and
       sections longer than config.CHUNK_SIZE split at blank lines rather than
       mid-sentence.

    Falls back to `fallback_split` for any document with no `##` headings at
    all, so bringing in a corpus that isn't sectioned still produces something.
    """
    limit = config.CHUNK_SIZE

    chunks: list[Chunk] = []
    for doc in documents:
        title_match = TITLE_LINE.search(doc.text)
        title = f"# {title_match.group(1)}" if title_match else f"# {doc.source}"

        parts = [p.strip() for p in SECTION_START.split(doc.text) if p.strip()]

        # Nothing sectioned in here — hand it to the original chunker.
        if len(parts) < 2:
            chunks.extend(fallback_split([doc]))
            continue

        bodies: list[str] = []
        for part in parts:
            # The first part is the title plus the opening paragraph. Drop the
            # title line, since it gets prepended to every chunk below anyway.
            if not part.startswith("##"):
                part = TITLE_LINE.sub("", part).strip()
                if not part:
                    continue

            for piece in _split_long_section(part, limit):
                # Too short to stand alone: fold it into the previous section.
                if bodies and len(piece) < MIN_CHUNK:
                    bodies[-1] = f"{bodies[-1]}\n\n{piece}"
                else:
                    bodies.append(piece)

        for index, body in enumerate(bodies):
            chunks.append(
                Chunk(
                    text=f"{title}\n\n{body}",
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
