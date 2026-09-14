# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** one `##` section, 900-character ceiling (94 chunks, 322 average,
shortest 174, longest 762)
**Overlap:** 0 characters, plus the document's `# Title` repeated on every chunk

I don't cut on a character count at all. Every document in `city_guides` is
already divided into labelled sections — *Getting there*, *Eat and drink*,
*When to go* — and each section is a self-contained answer to one question. The
section is the unit of meaning here, so that is what `split_documents` cuts on.
900 is a ceiling rather than a target: I measured the corpus first and its 84
sections run 176–711 characters, so nothing real is near the limit and it only
catches something unusually long, which it then splits at a blank line rather
than mid-sentence.

The starter's fixed 800-character window gave 51 chunks with a **shortest of
24** — a heading with nothing underneath it, which cannot answer anything and
still occupies a top-k slot. Mine reports a shortest of 174.

**Overlap is 0, and that is a decision rather than an oversight.** Overlap
exists to rescue a sentence cut in half, and a section boundary never cuts one.
What a section split *does* lose is which town the section is about: nine of my
fourteen documents contain a section called "Getting there", and Kestrelford's
is word-for-word indistinguishable from Halden Bay's once the filename is gone.
So instead of 120 characters of shared prose, every chunk repeats its
document's title — about 12 characters of context that says which place this is.

**I tested that decision instead of assuming it.** I built a second index with
the titles stripped (`--variant`) and asked both indexes where the chunk
containing the answer ranked:

| Question | With title | No title |
|---|---|---|
| How often do Marchwood's trams run on a weekday? | #1 (0.255) | #2 (0.404) |
| What time does the Kestrelford bakery sell out? | #1 (0.336) | #3 (0.494) |
| Can I reach Elder Ness by public transport? | #5 (0.477) | #18 (0.735) |
| How early to park in Halden Bay on a summer weekend? | #3 (0.352) | #7 (0.495) |
| Which town is the best bet for a winter visit? | #3 (0.539) | #2 (0.505) |
| How do I get to Kestrelford? | #7 (0.483) | #56 (0.762) |

Five of the six improve, one badly — without the title, "how do I get to
Kestrelford?" falls from 7th to 56th.

**What I got wrong on the way.** My first reaction to that last row was that the
repeated title was the problem: it makes all nine Kestrelford chunks
near-equally similar to any question naming the town, which flattens the
distances and drowns the section signal. The experiment says the opposite — the
title is load-bearing, and #7 is a different fault. Kestrelford's "Getting
there" section never uses the word Kestrelford in its body and is written as a
list of negatives ("No railway station"), while "Getting around" is lexically
closer to "get to" than "Getting there" is. That is a retrieval-stage problem,
not a chunking one, and it is the first thing I'll look at in week 2.

## Sample Chunks

All five are the unedited output of `python app.py chunks -n 5`, which samples
across the corpus rather than taking the first five of one document.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

**Reading them against the test.** Chunks 2 through 5 each stand on their own:
you could answer *"where do I stay in Corry Vale?"* or *"when should I go to
Pellew Sands?"* from the chunk alone, without reading anything before or after
it, and the title line tells you which place is being discussed.

**Chunk 1 is the weak one, and it is the shortest chunk in the index at 174
characters.** It is a document preamble rather than a section — the framing
paragraph that sits above the first `##` heading. It says the guide is honest
rather than promotional, which is true and answers no question anyone would
ask. This is the 1 in criterion 4's "at least 4 of 5", and it is the case that
criterion predicted: preambles are useful in the town guides, where the opening
paragraph carries real facts (*"Kestrelford is a hill town of 12,000"*), and
near-empty in the five cross-cutting guides, where it is only framing. Folding
short preambles into the section that follows them is the obvious fix, and I
have deliberately left it for week 2 rather than tuning it away now.

## Sample Answer

**Question:** Which town in the region is the best bet for a winter visit?

**Answer:**

```
  (best distance 0.511, cutoff 0.55)

Marchwood is the best bet for a winter visit because almost everything is
indoors and nothing closes seasonally. (Source: `guide_marchwood.md`)

Thornby Wells is also noted as the region's most reliable winter destination
after Marchwood, due to its concert season running from September to April.
(Source: `guide_thornby_wells.md`)

Sources retrieved: guide_halden_bay.md, guide_kestrelford.md,
guide_marchwood.md, guide_thornby_wells.md, guide_walking.md
```

This is the question I wrote expecting it to fail. No sentence in the corpus
answers it — the system had to weigh Marchwood's *"the one place in the region
that works in winter"* against Thornby Wells's *"the region's most reliable
winter destination after Marchwood"*, in two documents that never mention each
other. It got both, in the right order, and cited both.

**Both grounding layers, tested separately.** The gate is the first layer and
the prompt is the second. To check the second one actually does something, I
raised the cutoff past a question I know is uncovered:

```
$ python app.py ask "what is the best hotel in Paris?" --threshold 0.7
  (best distance 0.583, cutoff 0.7)

I don't have enough information to answer your question, as Paris is not
mentioned in the provided documents.
```

Retrieval handed it five "Where to stay" chunks and it refused anyway. At my
real cutoff of 0.55 that question never reaches the model at all.

**My relevance cutoff: 0.55**

| Question | In corpus? | Best distance |
|---|---|---|
| How often do Marchwood's trams run on a weekday? | Yes | 0.255 |
| How early to park in Halden Bay on a summer weekend? | Yes | 0.299 |
| What time does the Kestrelford bakery sell out? | Yes | 0.336 |
| Can I reach Elder Ness by public transport? | Yes | 0.357 |
| Which town is the best bet for a winter visit? | Yes | 0.511 |
| What is the capital of Mongolia? | No | 0.803 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835 |
| How do I write a for loop in Rust? | No | 0.836 |
| How do I change the oil in a diesel engine? | No | 0.888 |
| Who won the 1994 World Cup? | No | 0.975 |

**Why 0.55 and not 0.6.** Those ten rows on their own are misleading. They show
a gap between 0.511 and 0.803 — nearly 0.3 wide — and any number in it looks
equally defensible, including the 0.6 the starter ships with. That is an
artefact of the out-of-corpus questions being from another planet: Mongolia,
diesel engines, the 1994 World Cup. Nothing about my corpus made that gap wide;
the questions did.

So I measured five **near** misses as well — travel-shaped questions that this
corpus still does not cover:

| Near-miss question | Best distance |
|---|---|
| What is the best hotel in Paris? | 0.583 |
| How much does the train to Edinburgh cost? | 0.583 |
| Which dorm has the mould problem? | 0.686 |
| Is the housing lottery random? | 0.773 |
| Do I need a visa to visit? | 0.846 |

The real gap is **0.511 to 0.583**, and it is 0.072 wide rather than 0.292.
0.55 sits in it. The default 0.6 would have answered a question about hotels in
Paris out of guides to a region that contains no Paris.

**What this costs me.** 0.55 leaves only 0.039 of headroom above my hardest
real question. A question harder than the hardest one I thought to write gets
refused, and I only have five in-corpus measurements to judge that from. I
chose that over the alternative: at 0.6 the system confidently answers
travel-shaped questions about places that aren't in the corpus, and a wrong
answer that names a real filename is harder for a reader to catch than a
refusal. If week 2 shows real questions being refused, this number is the first
thing I'll revisit.

**Top-k stays at 5.** Worth noting that top-k has no effect on the gate at all:
I measured every in-corpus question at k=3, 5 and 8 and the best distance was
identical to three decimal places in all three, because the best distance is
rank 1 by definition. Top-k only changes how much material the model sees after
the gate has already decided. 5 is enough that the winter question got both
towns it needed, and small enough that the answer above cites 2 documents
rather than drowning in 8.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
