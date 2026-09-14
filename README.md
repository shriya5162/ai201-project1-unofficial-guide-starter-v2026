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

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

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
