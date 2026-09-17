# academic-manuscript-review

A Claude skill for pre-submission diagnostic review of academic manuscripts in management, organization theory, strategy, and adjacent social-science fields, at the standard of AMJ, ASQ, AMR, SMJ, and Organization Science.

This is a diagnostic tool for authors, not a peer-review simulator. It is exhaustive where a real reviewer would prioritize, direct where a real reviewer would cushion, and non-repetitive by rule: every issue is flagged once, explained, and paired with a fix. The design rationale, source materials, and test results are documented in the build log: https://galblatman.com/blog/teaching-claude-to-review-like-an-editor/.

## Install

1. Claude (web or desktop): Settings, then Capabilities, then Skills, then upload `academic-manuscript-review.zip`.
2. In any chat, upload a manuscript and ask for a review. The skill triggers on natural phrasings: "fresh eyes on this draft," "thoughts on this paper," "tear this apart," "pre-submission read."

## What's inside

- `SKILL.md`: the operating stance, input handling for messy drafts (tracked changes, Word comments, placeholder tables, inline TODOs), and a twelve-section review protocol ending in a prioritized revision plan.
- `references/tone_and_register.md`: voice calibration drawn from real top-tier decision letters, presented as reconstructions in each letter's register rather than quotations, plus eight named anti-patterns drawn from an AI-generated review.
- `references/exhaustive_checklist.md`: the scanning catalog for the section-by-section sweep, including numerical-consistency checks, construct-drift checks, and an opt-in reference style audit keyed to journal conventions.

## Usage notes

- The always-on citation check verifies internal consistency (every in-text citation appears in the reference list and vice versa). It does not verify that cited works exist. Independently verify any specific citation the review names before acting on it; language models fabricate plausible references.
- The reference style audit is opt-in. Ask "check my references" and name the target journal or style.
- Scope the review if you want less: "review only the theory section" works.
- The skill reviews revised drafts as standalone manuscripts. It does not evaluate response letters or referee rebuttals.

## Provenance

Version 2, first public release. Built from three published *Academy of Management Review* editorial essays on reviewing (Ragins, 2015; Ballinger & Johnson, 2015; Lepak, 2009), two real decision letters from top management journals, one AI-generated review used as a negative exemplar, and the author's own review protocols. Tested against a manuscript with a known editorial outcome before release.

The decision letters are not reproduced here. What ships are reconstructions written in each letter's register, preserving the rhetorical moves but not the words, the content, or any identifying detail. Editors and reviewers write those letters with an expectation of confidentiality.

References:

- Ballinger, G. A., & Johnson, R. E. 2015. Editors' comments: Your first AMR review. *Academy of Management Review*, 40: 315-322.
- Lepak, D. 2009. Editor's comments: What is good reviewing? *Academy of Management Review*, 34: 375-381.
- Ragins, B. R. 2015. Editor's comments: Developing our authors. *Academy of Management Review*, 40: 1-8.

No license granted yet; contact me before redistributing or adapting. Feedback, bug reports, and reviews the skill got wrong: Gal.Blatman@marshall.usc.edu, or the comments on the build-log post.
