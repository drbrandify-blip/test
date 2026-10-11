# Pathology: All-in-One — Special Pathology for 4th Year MBBS (Modules 10–12)

First edition draft, October 2026. A4, two-colour print (black + haematoxylin purple #5b2a86).
Standard text: Robbins (Basic Pathology / Pathologic Basis of Disease, 10th ed). Syllabus: the user's 4th-year syllabus (BUMDC pattern, UHS-compatible).

## Output
- `../deliverables/Pathology All-in-One - Special Pathology 4th Year MBBS.pdf` — complete book with covers and bookmarks: 391 PDF pages (covers + xv prelims + blank + 373 numbered pages).
- `../deliverables/Pathology All-in-One - Print files and source.zip` — print-ready interior PDF, cover PDF, cover preview PNG and the full source.

## Contents
Front: title + copyright, how to use (legend of all box types), syllabus map (every lecture/interactive/lab → chapter), exam craft (SEQ, gross specimen, slide, data stations, BCQ, viva), study plans + 31-row tracker.

31 chapters in 11 parts:
A GIT: 01 Oral cavity, salivary glands & oesophagus · 02 Stomach · 03 Malabsorption & IBD · 04 Polyps & colorectal carcinoma
B Liver/GB/pancreas: 05 Jaundice & viral hepatitis · 06 Cirrhosis, haemochromatosis & HCC · 07 Gallbladder & pancreas
C Lung: 08 Pneumonia & TB · 09 COPD, asthma & ILD · 10 Lung tumours
D Blood: 11 Anaemias I · 12 Haemolytic anaemias & thalassaemias · 13 Leukaemias & MPN · 14 Lymphomas & plasma cell neoplasms · 15 Bleeding disorders
E Kidney: 16 Glomerular diseases · 17 Tubulointerstitial, cystic kidney, RFTs & acid–base · 18 Renal & urothelial tumours, urolithiasis
F Reproductive & breast: 19 Prostate & testis · 20 Vulva, cervix & endometrium · 21 Ovary & GTD · 22 Breast
G Endocrine: 23 Thyroid & parathyroid · 24 Pituitary, adrenal & diabetes
H CVS: 25 Blood vessels · 26 Heart
I MSK: 27 Bone · 28 Joints & skeletal muscle
J CNS: 29 CNS I (vascular, infections, demyelinating, degenerative) · 30 CNS II (tumours, nerve sheath)
K Skin: 31 Skin

Back: master tables (genes/translocations, markers/IHC, stains, eponymous cells & bodies), buzzwords A–Z (189), lab OSPE atlas (37 slide cards + gross tables), top 60 SEQ themes, grand mock paper (45 BCQs + 9 SEQs + marking scheme), last-day checklist.

Totals in chapters: 118 solved SEQs, 379 BCQs (+45 mock), 377 viva, 98 OSPE stations, 141 gross/microscopy panels, 185 tables, 31 mind maps, 94 flowcharts, 26 chevron timelines, 6 original illustrations (glomerular deposit map, peptic ulcer zones, emphysema types, bone-tumour sites, aortic dissection types, blister levels).

## Chapter template
meta (Exam Radar, objectives, hook, Robbins link) → mind map → numbered concept sections (Definition, Concept Clear, Pakistan Focus, Memory Hook, Exam Trap, Lab Values, Clinical Case, Clinical Correlation, Molecular Key, Lab Spotter boxes; gross | microscopy panels; tables; flowcharts) → Exam Zone (pattern SEQs with model answer plans; 12 BCQs with keys; 12 viva; OSPE stations) → Night-before page.

## Build
Requirements: Python 3 with playwright (Chromium at /opt/pw-browsers or edit `CHROME` in tools/build.py), beautifulsoup4, pypdf, pdfplumber, reportlab, pillow, fonttools; graphviz `dot`; poppler-utils.
- Fonts: `python3 tools/make_fonts.py` (needs Lora variable TTFs in /tmp and Inter OTFs; static fonts are already in assets/fonts).
- One chapter preview: `python3 tools/build.py ch16` → `build/ch16.pdf`; contact sheet `python3 tools/sheet.py build/ch16.pdf`.
- Whole book: `python3 tools/assemble.py` → `build/BOOK_full.pdf`, `BOOK_interior_print.pdf`, `BOOK_cover.pdf`.
- Writers' rules: `STYLE_GUIDE.md`. Chapter plan and syllabus mapping: `sources/chapters.md`. Pakistan facts: `sources/facts_pk.md`.

## Quality checks done
- Every chapter built and checked on contact sheets by its writer; automated scan for near-empty pages.
- Independent examiner review of all 379 BCQ keys and 377 viva answers against Robbins: 2 corrections + 5 wording tightenings applied.

## Open items
- Placeholders to fill: compiler/author name, © holder, ISBN + barcode, price, publisher, printer, corrections e-mail (title page, copyright page, front and back covers).
- SEQs are "Prof pattern / Module pattern / Classic" questions modelled on recurring BUMDC/UHS themes; no real past-paper files for pathology were reachable (Drive search showed only one Module 12 OSPE note file). If the college past papers are supplied, real questions can be tagged with their source and year.
- Robbins PDF (27 MB, Drive file "robin book.pdf") could not be downloaded in the cloud environment (Drive connector limit 10 MB; drive.google.com blocked by the network policy). Facts were written from Robbins knowledge; writers' flagged items are listed in their reports — a page-level check against the PDF is still possible if it is attached directly.
- Covers are exact A4 without bleed; add 3 mm bleed if the printer requires it.
