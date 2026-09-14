"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in week 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in week 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # Answer sits in one sentence, in two documents that agree.
    # guide_marchwood.md "Getting around", guide_accessibility.md "Straightforward".
    {"question": "How often do Marchwood's trams run on a weekday?", "expects": "8 minutes"},

    # Answer sits in one sentence, stated twice in the same words.
    # guide_kestrelford.md "Eat and drink", guide_eating.md "Local specifics".
    {"question": "What time does the Kestrelford bakery sell out?", "expects": "11am"},

    # A negative fact. The answer is that a thing does not exist, which is
    # harder to retrieve than a fact about a thing that does.
    # guide_elder_ness.md "Getting there".
    {"question": "Can I reach Elder Ness by public transport?", "expects": "no public transport"},

    # Answer is one sentence but three documents state it in different words
    # ("fill by 10am", "arrive before 10am", "both lots fill by 10am").
    # guide_halden_bay.md, guide_seasons.md, guide_regional_transport.md.
    {"question": "How early do I need to arrive to park in Halden Bay on a summer weekend?", "expects": "10am"},

    # The hard one. No single sentence answers this: it needs Marchwood's "the
    # one place in the region that works in winter" weighed against Thornby
    # Wells's "the region's most reliable winter destination after Marchwood".
    # Two documents, a comparison, and no shared wording with the question.
    {"question": "Which town in the region is the best bet for a winter visit?", "expects": "Marchwood"},
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
