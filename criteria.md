# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next week costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Four of my questions are answered by a single sentence that
appears in at least two documents. The fifth — which town is the best bet in
winter — is answered by no sentence anywhere: it needs Marchwood weighed against
Thornby Wells, and shares no wording with either. That is the one I expect to
miss.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** `generate.py::build_prompt` labels every excerpt
`[from <filename>]` and `GROUNDING_INSTRUCTION` tells the model to name it, so
the filename is in front of the model on every call. A miss would mean the model
ignored an explicit instruction, not that the task was hard — and 4 of 5 would
quietly excuse that.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** In Milestone 1 the in-corpus Kestrelford question measured
0.445 and the out-of-corpus housing-lottery question 0.773 — a wide gap either
side of the default 0.6. Not 5 of 5, because my guides are full of "where to
stay" and an out-of-corpus question about accommodation could sit close enough
to slip under. Full ten-question measurement in Milestone 4.

---

## 4. Chunks begin at a heading and end at a sentence

The `shortest` figure reported by `python app.py index` is at least 150
characters, and of the five chunks printed by `python app.py chunks -n 5`, at
least 4 begin at a `##` section heading and end at a sentence boundary rather
than mid-sentence.

**Why this target:** Each document is cut into labelled `##` sections and each
section is a self-contained answer, so the section is the unit of meaning here,
not the character count — but the shipped 800-character window gave me 51 chunks
with a shortest of 24, which can only be a heading with nothing under it. I set
the floor at 150 because the corpus's 84 sections run 176–711 characters, so 150
catches that fragment without condemning my genuinely shortest section. 4 of 5
rather than 5 because each document's last section has no following heading to
stop at.



---

## 5. The source named is the source the answer came from

For all 5 test questions, the document the answer names in its own text actually
contains the fact stated — checked by opening that file and finding the
sentence.

**Why this target:** Criterion 2 only asks that a source is *named*, and
`app.py` prints a `Sources retrieved:` line from retrieval metadata whether or
not the model cited anything, so criterion 2 can pass while the citation is
absent or wrong. Nine of my 14 documents end with the same boilerplate
paragraph, which makes a plausible-but-wrong filename easy to produce. 5 of 5
because a confident answer attached to the wrong file is the one error a reader
has no way to catch.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in week 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
