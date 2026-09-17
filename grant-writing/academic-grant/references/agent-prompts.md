# Agent Prompt Templates — Academic Grant Skill

This file contains reusable prompt templates for each agent dispatched during the grant writing workflow. Copy the relevant template into your Agent tool call, filling in the placeholders.

---

## Section Drafting Agent

**When to use:** Phase 2 — one per grant form section.

**Prompt template:**

```
You are drafting [SECTION_NAME] of a grant application for a research project on [PROJECT_TOPIC].

**YOUR TASK:** Write [SECTION_NAME] following the STRUCTURE and STYLE of the sample below. Save your output to [OUTPUT_PATH].

**FORM STRUCTURE (from the blank form):**
```
[EXACT_SECTION_STRUCTURE_FROM_FORM]
```

**SAMPLE STYLE (from a different project — follow its paragraph structure, citation style, and level of detail):**
[RELEVANT_EXCERPT_FROM_SAMPLE_DOC]

**SOURCE MATERIAL — Read these files:**
1. [SOURCE_PATH_1] — [description]
2. [SOURCE_PATH_2] — [description]

**SECTION GUIDANCE:**
[2-3 bullets about what content to include, specific findings to report, key citations]

**STYLE RULES:**
- Academic economics/finance tone, like the sample
- Use inline citations: Author (Year) or (Author, Year)
- [number] paragraphs, one per [unit]
- Each paragraph: state [element], explain why it matters, briefly preview the approach
- Write in first-person plural ("we")
- Target [word count range]
- Do NOT use markdown formatting like bold headers within the body — use plain text section titles
- Save immediately to the output file path above

**IMPORTANT:** Save your completed section to: [OUTPUT_PATH]
Do NOT return the full text to the main agent. Only return a brief status summary.
```

---

## Review Agent

**When to use:** Phase 3 — after all section drafting agents complete.

**Prompt template:**

```
You are reviewing a grant application draft for quality, completeness, and consistency.

**YOUR TASK:** Read all drafted sections and the sample application. Write a review with specific feedback for each section. Save your output to [REVIEW_PATH].

**FILES TO READ:**
1. Sample (for structure/style reference): [SAMPLE_PATH]
2. [List all section files]

**FORM STRUCTURE (must be followed exactly):**
[List the expected section hierarchy]

**REVIEW CRITERIA:**
1. **Structure compliance** — Does each section match the form structure?
2. **Completeness** — Does every section cover all required content?
3. **Consistency** — Do sections reference each other correctly? Terminology consistent?
4. **Style** — Academic tone? First-person plural ("we")? Inline citations correct?
5. **Accuracy** — Are coefficients, p-values, and findings reported correctly?
6. **Flow** — Do sections transition naturally? Narrative coherent?
7. **Gaps** — Any important findings or details from the source material omitted?

**OUTPUT FORMAT:**
Write your review as a structured document with:
- A score (0-100) for each section
- Specific issues listed for each section with severity (Critical / Major / Minor)
- A list of cross-section consistency issues in a table
- A summary verdict (PASS / REVISE / MAJOR REVISION)
- Action items prioritized by severity

Save to: [REVIEW_PATH]
```

---

## Revision + Assembly Agent

**When to use:** Phase 4 — after review completes.

**Prompt template:**

```
You are the final revision and assembly agent for a grant application. Your job is to:
1. Read all drafted sections
2. Read the review feedback
3. Apply ALL required revisions
4. Assemble into a single final document
5. Run the DOCX conversion script

**INPUT FILES (read all):**
1. [SECTION_1_PATH]
2. [SECTION_2_PATH]
...
N. [REVIEW_FEEDBACK_PATH]

**REQUIRED REVISIONS (from review — address ALL of these):**
[List each major issue from the review]

**ASSEMBLY INSTRUCTIONS:**
After making all revisions, assemble the sections into a single document in the correct order.
Remove all markdown header symbols (#). Use plain bold text for section headers (**1. Section Name**).
Convert LaTeX math to plain text notation.

Save the assembled markdown to: [ASSEMBLED_MD_PATH]

Then convert to DOCX:
```
python scripts/assemble_docx.py [ASSEMBLED_MD_PATH] [OUTPUT_DOCX_PATH]
```

The script auto-installs python-docx if missing.

Save BOTH the assembled markdown AND produce the DOCX. Run the script with Bash.
```

---

## Citation Extraction Agent A (In-text Citations)

**When to use:** Phase 5 — reads the assembled project statement.

**Prompt template:**

```
Extract EVERY in-text citation from the grant application.

Read: [ASSEMBLED_MD_PATH]

Extract all citations in the form Author (Year), (Author, Year), (Author et al., Year).
For each citation found, list:
1. Full author name(s) as cited
2. Year
3. Which section it appears in

Output format: Author(s) | Year | Section
Sort alphabetically by author. Note duplicates.

Save to: [CITATIONS_EXTRACTED_PATH]
```

---

## Citation Extraction Agent B (Reference Entries)

**When to use:** Phase 5 — reads the references document.

**Prompt template:**

```
Extract every reference entry from the references document.

Read: [REFERENCES_MD_PATH]

For each reference, extract: Author(s), Year, Title (first 60 chars), Journal/Publisher, Volume/Issue/Pages.

Output format: Author(s) | Year | Title | Journal | Volume/Issue/Pages?
Sort alphabetically by author. Count total references.

Save to: [REFERENCES_EXTRACTED_PATH]
```

---

## Citation Verification Agent

**When to use:** Phase 5 — verify metadata for each reference via web search.

**Prompt template:**

```
Verify bibliographic metadata for each reference. Search the web to confirm journal name, volume, pages, and year.

Read: [REFERENCES_MD_PATH]

For each reference, verify:
1. Is the journal name correct?
2. Is the year correct?
3. Are volume and page numbers correct?
4. Is the title correct?

Focus on references where metadata errors are common (forthcoming articles, working papers, recent publications).

Output format per reference:
STATUS: CORRECT / ERROR / UNCERTAIN
Author(s) | Year | Found: [actual from search] | Listed: [in our references]

Save to: [CITATION_VERIFICATION_PATH]
```

---

## Supporting Document Agent

**When to use:** Phase 6 — one per supporting document (Education Plan, Pathway to Impact, References).

**Prompt template:**

```
You are drafting [DOCUMENT_NAME] for a grant application.

**YOUR TASK:** Write the [DOCUMENT_NAME] following the sample structure. Save to [OUTPUT_PATH].

**SAMPLE:**
Read [SAMPLE_PATH] for structure and tone.

**PROJECT CONTEXT:**
Read the completed project statement: [PROJECT_STATEMENT_PATH]
Key findings to reference: [BRIEF_SUMMARY]

**STRUCTURE TO FOLLOW:**
[List the expected structure from the sample]

**STYLE:**
- Match the sample's tone — concise, professional
- Do not use markdown headers or bold formatting (except document title)
- Target [word count]
- Use "The PI" and "the project" as in the sample

Save to: [OUTPUT_PATH]
```

---

## Cross-check Rules (Main Agent)

After Phase 5 agents complete, the main agent must:

1. Read `citations_extracted.txt` and `references_extracted.txt`
2. Build two sets:
   - Set A: all works cited in-text
   - Set B: all works in the reference list
3. Report mismatches:
   - **Cited but not referenced:** works in A but not B → must add to references
   - **Referenced but not cited:** works in B but not A → consider removing
   - **Year mismatches:** same author(s) but different years
4. Read `citation_verification.txt` for metadata errors
5. Apply fixes to the references file and re-generate the DOCX
