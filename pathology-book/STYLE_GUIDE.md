# "Pathology: All-in-One" — Special Pathology, 4th Year MBBS · Writer's Style Guide

You are writing chapters of a print book (A4, two-colour: black + haematoxylin purple #5b2a86) for 4th-year MBBS students in Pakistan (BUMDC/Bahria pattern, UHS-compatible). It will be printed cheaply and sold, so it must read like a professionally edited, original review book. The standard text is **Robbins** (Basic Pathology / Pathologic Basis of Disease, 10th ed): definitions, classifications, morphology and numbers must agree with Robbins. Where teachers or other books differ, give the Robbins version and note the variant in an Exam Trap box.

The goal: **short but complete**. A student who knows this chapter can answer any SEQ, BCQ, viva, OSPE slide or gross-specimen question on the topic. Concepts must be crystal-clear (the WHY), memorable (hooks, flowcharts, tables) and never boring.

**The exemplar chapter is `chapters/ch16.html`. Read it fully before writing.** Copy its structure, tone, density and component usage. Its rendered PDF is `build/ch16.pdf`; look at 2–3 pages (e.g. `python3 tools/sheet.py build/ch16.pdf` then Read the PNG in `build/sheets/`).

## 1. Chapter structure (in this order)
1. `<script type="application/json" class="meta">` — fields: `ch` (int), `part` (A–K, see sources/chapters.md), `title`, `short` (≤ 40 chars, running head), `hook` (1–2 vivid sentences), `objectives` (5–7, start with a verb), `radar` (keys exactly `SEQ`, `BCQ`, `Viva`, `OSPE`; 1–3 stars), `radar_note` (one line on why/what is asked; do NOT invent counts or years), `robbins` (Robbins chapter title in italics + topics, no page numbers).
2. A **mind map** `div.mm` — 5–7 branches, 2–4 items each (≤ 45 characters per item; `**bold**` allowed).
3. **Concept sections** `h2` with `<span class="sn">N.1</span>` numbering (N = chapter number), 4–7 sections; `h3`/`h4` sub-heads. For every disease follow the Robbins rhythm, compressed: **definition → aetiology/risk → pathogenesis (flowchart if it is a sequence) → morphology (`div.morph` gross | microscopy) → clinical features / labs → complications / prognosis**. Skip a heading when there is nothing exam-worthy to say.
4. `<section class="exam-zone">` with, in order:
   - `<div class="zone-title"><span class="tag">EXAM ZONE</span> Past-Paper Pattern SEQs — Solved</div>` then **3–5 `.seq` blocks**: realistic BUMDC/UHS-style questions (scenario or "define/classify/describe" with marks split like 2+3 or 1+2+2). Tag `.src` honestly: `Prof pattern` (annual/professional style), `Module pattern` (module-exam style), or `Classic` (a perennially repeated theme). Never invent a year or "UHS 2019"-type source. Each has a "Model answer plan" listing exactly what earns the marks, plus a `.tip` "Score booster" where useful.
   - `<div class="zone-title a"><span class="tag">BCQs</span> One-Best-Answer Practice</div>` then a `div.mcqset` JSON list of **12 ORIGINAL one-best-answer MCQs** (5 options A–E, scenario-based where possible, testing the facts examiners repeat). Key + one-line reason. Spread correct letters across A–E (each letter 2–3 times). Double-check every key against Robbins.
   - `<div class="zone-title"><span class="tag">VIVA</span> Rapid-Fire Viva Voce</div>` then `div.vivaset` JSON of **12** `["question","answer"]` pairs (answers ≤ 25 words).
   - `<div class="zone-title a"><span class="tag">OSPE</span> Practice Stations</div>` then **2–4 `.osce` stations**: slide identification (describe what is seen under the microscope in words; give the diagnosis + 2 features + 1 related question), gross specimen, peripheral smear/marrow, or data interpretation (LFT, RFT/ABG, CSF, coagulation, thyroid profile, serology). Use `digests/ospe_lab.md` (the syllabus lab list) so every lab slide of your chapter appears as a station or Lab Spotter box.
5. `<section class="revision">` — "Rapid Revision · The Night-Before Page", copy the ch16 markup exactly: `.rr-grid` with 15 one-liners (left), Memory hooks `.rr.dark` + fill-the-gaps `.rr.grey` with 6 blanks + answers (right), `.draw-grid` with two chapter-specific draw-from-memory prompts, and the `.tracker`.

## 2. Components (defined in assets/book.css; see ch16 for exact markup)
- Boxes (`div.box.<kind>`; any box can take `data-label="..."`):
  `def` Definition (`<span class="term">Term</span>`; Robbins-faithful wording in your own words) · `concept` Concept Clear (the WHY — use generously, this is what makes the book special) · `pk` Pakistan Focus (only facts from `sources/facts_pk.md`; add `p.src-note` if a source is named) · `hook` Memory Hook (`p.big` for the mnemonic) · `trap` Exam Trap (look-alikes, classic MCQ traps, Robbins-vs-teacher variants) · `formula` Lab Values (normal ranges, cut-offs, test interpretation) · `worked` Clinical Case (vignette → reasoning → diagnosis) · `practice` Clinical Correlation · `molec` Molecular Key (genes, translocations, markers, IHC) · `spot` Lab Spotter (how to recognise the slide/specimen in the lab exam in 10 seconds).
- **Morphology panel** (use for every important disease):
  `<div class="morph"><div class="gross"><ul>…</ul></div><div class="micro"><ul>…</ul></div><div class="full">optional full-width note</div></div>` — headings "Gross"/"Microscopy" are added automatically (rename with `data-label` on the inner div, e.g. `data-label="Peripheral smear"`).
- Tables: `table.t` (+ `caption`, `thead`), `table.t.vs` for "A vs B" comparisons (first header cell black), `table.t.plain`. **Comparison tables are gold** — use one for every "differentiate between" pair examiners like.
- Lists: `ul`, `ul.cols2`, `ul.tight`, `ol.stepper`, `ol.frame` (`<li><b>Label</b> — text</li>`), layout `div.two`, `div.three`.
- Inline: `.kw` keyword, `.num` number, `.hl` highlighter, `.chip`.
- Diagrams (build script converts to SVG; `data-cap="<b>Figure N.x · Title.</b> text"`):
  - `div.mm` mind map (JSON).
  - `div.flow` flowchart (plain text, one chain per line `A -> B -> C`; prefixes `*` purple node, `!` black node, `?` decision diamond, `~` grey dashed node; edge label `A -[yes]-> B`; identical text = same node, so you can branch). `data-dir="LR"` for left-to-right, `data-w="22"` wrap width. Labels ≤ 6 words, ≤ 10 nodes. **Pathogenesis = flowchart.** Wide, short flowcharts (LR or 2–3 ranks) save space; very tall single-column flows waste a page — put a tall flow inside `div.two` next to text.
  - `div.cycle` `{"center": "...", "steps": [{"t": "...", "s": "..."}]}`; `div.stages` horizontal chevrons `{"items": [{"t": "...", "s": "..."}]}` (≤ 6) — ideal for sequences like adenoma–carcinoma, MI timeline, stages of lobar pneumonia; `div.line` `{"x": [...], "series": [{"name": "...", "y": [...]}], "ylabel": "...", "yticks": false}` for curves (cardiac markers, HBV serology); `div.bar`.
  - `div.illus` with `data-src="file.svg"` includes a pre-drawn illustration from `illus/` (only files that exist; you may draw one simple, accurate SVG yourself with a small Python script in `illus/` like `illus/glom_deposits.py` if a picture is essential — max 1 per chapter).
  - 4–7 diagrams per chapter including the mind map. Every diagram must be accurate and add meaning.
- MCQ JSON: `[{"q": "stem", "o": ["A","B","C","D","E"], "a": "C", "e": "reason"}]`. Viva JSON: `[["Q","A"], ...]`. **JSON must be valid**: no unescaped double quotes inside strings (use “ ” or ’), no trailing commas.

## 3. Voice & writing rules
- British/Pakistani English (haemoglobin, oesophagus, tumour, anaemia, oedema, programme). Keep official names.
- Concept-first: one or two lines of WHY before the WHAT. Short paragraphs (≤ 4 lines); bullets ≤ 2 lines; bold the mark-earning words.
- Morphology language must be precise (gross: size, colour, consistency, cut surface; micro: architecture → cells → special features). These are the words examiners look for.
- Molecular genetics: give the key gene/translocation and what it does, in one line. No unnecessary depth.
- Mnemonics: 1–3 per chapter, genuinely helpful, accurate, not childish.
- **Originality (this book will be sold):** write in your own words. Do NOT copy sentences from Robbins or any source. Standard definitions may be paraphrased closely. MCQs, SEQ answers and cases must be your own.
- No emojis, no filler ("In conclusion", "this chapter will…"), no mention of AI, digests, sources files or "the notes say".
- Numbers: use Robbins figures; when Robbins gives a range, give the range or "about". Never invent precise statistics.
- **Length: 8–10 rendered A4 pages** per chapter (★ chapters in sources/chapters.md may reach 11–12). Short but complete: everything needed for SEQ, BCQ, viva and OSPE — nothing more.

## 4. Sources
- Plan & exact topic list per chapter: `sources/chapters.md` (cover every listed item; do not drift into other chapters' topics — cross-refer instead, e.g. "see Chapter 24").
- Lab/OSPE list and the Module 12 OSPE notes: `digests/ospe_lab.md`.
- Pakistan facts: `sources/facts_pk.md`.
- Robbins text: if `sources/robbins/` contains extracted chapter text files (`pbd_chNN.txt`), use `grep -n -i` to VERIFY specific facts/numbers (do not read whole chapters; it wastes budget). Otherwise rely on your own knowledge of Robbins.

## 5. Build & check (mandatory, but economical)
- Write `chapters/chXX.html` (fragment, no html/head). Build: `cd /home/user/test/pathology-book && python3 tools/build.py chXX` → prints page count. A JSON or graphviz error names the block — fix and rebuild.
- Check once visually: `python3 tools/sheet.py build/chXX.pdf` and Read the contact-sheet PNGs (8 pages per image). Fix: overflowing/ugly diagrams, near-empty pages, orphan headings, broken tables, page count outside 8–10 (trim or extend). Zoom only where needed: `pdftoppm -r 70 -f N -l N -png build/chXX.pdf build/sheets/z` and Read that one PNG. Do not render every page at high resolution.
- Then re-read your chapter once as an examiner: every MCQ key correct, facts consistent with Robbins, nothing outside the syllabus written at length.
- Do not edit `assets/book.css`, `tools/*.py` or other writers' chapters. If a component is missing or broken, report it.

## 6. Final message
Report briefly: chapters written, page counts, number of SEQs/MCQs/viva/OSPE per chapter, any facts you were unsure about (for the editor to verify), and any component problems.
