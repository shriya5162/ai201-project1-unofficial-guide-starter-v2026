"""
Settings for The Unofficial Guide.

Everything you're likely to change lives here, at the top, on purpose.
You'll edit THRESHOLD in Milestone 4 and the chunking numbers in Milestone 3.

Anything you set in your .env file wins over the defaults here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")


# ─── The corpus you're working with ──────────────────────────────────────────
# Change this to switch corpora, or pass --corpus on the command line.
# Options are the folder names inside corpora/. See corpora/README.md.

CORPUS = os.getenv("AI201_CORPUS", "city_guides")


# ─── Chunking (Milestone 3) ──────────────────────────────────────────────────
# These are deliberately plain, generic numbers. Milestone 3 is where you
# replace them with numbers that fit the documents you actually read.

# Milestone 3. chunker.py::split_documents cuts on `##` section headings, not
# on a character count, so these mean something slightly different now:
#
# CHUNK_SIZE is a CEILING, not a target. A section is left whole unless it
# exceeds this, in which case it splits at a blank line. The corpus's 84
# sections run 176–711 characters, so 900 leaves every real section intact and
# only catches something unusually long.
#
# CHUNK_OVERLAP is 0 because a section boundary is already a topic boundary —
# there is no half-finished sentence to rescue. The context that would
# otherwise be lost is restored by repeating the document's `# Title` on every
# chunk instead, which costs ~12 characters rather than 120.
CHUNK_SIZE = 900        # ceiling before a section is split at a blank line
CHUNK_OVERLAP = 0       # unused by the section chunker; fallback_split still reads it


# ─── Retrieval (Milestone 4) ─────────────────────────────────────────────────

TOP_K = 5               # how many chunks to pull back per question

# The relevance gate. If the best chunk is further away than this, the system
# refuses to answer instead of handing the model thin material.
#
# LOWER IS BETTER: 0.3 is a close match, 0.9 is unrelated.
#
# Milestone 4, measured rather than guessed. My two groups:
#
#   in corpus (5 questions)        0.255 – 0.511
#   out of corpus (OUT_OF_SCOPE)   0.803 – 0.975
#
# Those alone suggest anything from 0.52 to 0.80 works, because the shipped
# out-of-scope questions are from another planet entirely. So I also measured
# five NEAR misses — travel-shaped questions this corpus still doesn't cover:
#
#   "what is the best hotel in Paris?"            0.583
#   "how much does the train to Edinburgh cost?"  0.583
#   "which dorm has the mould problem?"           0.686
#
# The real gap is 0.511 to 0.583, not 0.511 to 0.803. 0.55 sits in it.
# The default 0.6 would have answered the Paris question out of guides to a
# region that has no Paris in it.
THRESHOLD = 0.55


# ─── Models ──────────────────────────────────────────────────────────────────
# Embeddings run on your own machine and cost no API quota.
# Only generation calls out to a service.

# This is the model Chroma bundles, and leaving it alone is the fast path: it
# downloads about 80 MB from Chroma's own CDN and needs nothing else installed.
#
# Setting it to any other name — week 2's "try a second embedding model"
# stretch option — switches to loading that model from Hugging Face instead,
# which needs `pip install 'sentence-transformers>=3.4,<3.5'` first. store.py
# says so with a real error message rather than a stack trace if you forget.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL = os.getenv("AI201_MODEL", "gemini-3.5-flash-lite")


# ─── Rate limiting and quota guards ──────────────────────────────────────────
# You should not need to touch these. They exist so that a runaway loop costs
# you a warning instead of your whole day's allowance.

REQUESTS_PER_MINUTE = 30       # outgoing calls the limiter will allow per minute
SESSION_REQUEST_BUDGET = 300   # stop and warn rather than draining the daily quota
MAX_RETRIES = 4                # on 429 / resource-exhausted, with backoff

CACHE_ENABLED = os.getenv("AI201_CACHE", "1") != "0"
CACHE_DIR = ROOT / ".cache"


# ─── Paths ───────────────────────────────────────────────────────────────────

CORPORA_DIR = ROOT / "corpora"
CHROMA_DIR = ROOT / "chroma_db"
RESULTS_DIR = ROOT / "results"


def corpus_path(name: str | None = None) -> Path:
    """Folder holding the documents for a corpus."""
    return CORPORA_DIR / (name or CORPUS) / "documents"


def collection_name(name: str | None = None, variant: str = "default") -> str:
    """
    Name of the vector-store collection for a corpus.

    `variant` lets you index the same corpus two different ways and query both
    without deleting anything — you'll want that in week 2 when you compare
    chunking strategies.

    Chroma is fussy about collection names: 3 to 63 characters, starting and
    ending with a letter or digit, and nothing but letters, digits, underscores
    and hyphens in between. If you bring your own corpus and name the folder
    something Chroma won't accept, this cleans it up rather than failing.
    """
    import re

    raw = f"{name or CORPUS}__{variant}"
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "-", raw)
    cleaned = cleaned.strip("_-")          # must start and end alphanumeric
    if not cleaned or not cleaned[0].isalnum():
        cleaned = f"c{cleaned}"
    if not cleaned[-1].isalnum():
        cleaned = f"{cleaned}0"
    return cleaned[:63].rstrip("_-") or "collection"
