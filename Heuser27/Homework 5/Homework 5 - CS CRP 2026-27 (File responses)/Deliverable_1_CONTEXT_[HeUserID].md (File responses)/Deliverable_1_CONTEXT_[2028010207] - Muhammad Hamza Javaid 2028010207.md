&#32;

# Project in one paragraph

This project is a personal digital library and knowledge-graph web application for research papers. A user uploads an academic paper as a PDF through the browser; the server stores the file, parses it to extract structured metadata (title, authors, abstract, keywords, DOI/arXiv ID, year, venue, and the reference list as separate records), automatically assigns topic tags, and persists everything in a SQLite database with relational tables linking papers, authors, topics, and references. Every upload, edit, tag change, and deletion is recorded in an activity log with the user's name and a timestamp, so the app remembers who did what and when. Users can browse, search, and filter the library, open a paper detail view to inspect and manually correct metadata, view the activity history, and delete papers. As more papers are added, the app draws an interactive knowledge graph connecting papers, authors, and topics (with derived edges such as co-authorship and co-occurring topics). The entire app must be built under strict no-build constraints: a Python backend, SQLite database, and vanilla HTML/CSS/JS frontend, with no Node.js, npm, JS frameworks, or build step.

# Anatomy of a research paper (sections, order, what each contains)

## **Typical anatomy of a research paper:**

| **Section (order)** | **Core content / purpose** | **Concrete example / note** |
| :--- | --- | --- |
| **1. Title** | Concise, descriptive statement of the paper’s subject; often names the treatment, organism, system, or key variables. | “Fry Grading prior to Stocking Improves the Production of Channel Catfish, _Ictalurus punctatus_, in Recirculating Aquaculture Systems”. Elsevier advises avoiding abbreviations and formulae in titles. |
| **2. Authors & affiliations** | Author names, institutional affiliations, corresponding-author contact details, sometimes membership grades or ORCID. | IEEE conference style requires each author’s **membership grade** (where applicable), **business affiliation**, **complete mailing address**, and optional e-mail/fax. Elsevier requires superscript letters linking authors to affiliations and a clearly marked corresponding author. |
| **3. Abstract** | Self-contained summary of the problem, approach, principal results, and conclusions; usually 125–250 words; no references, figures, or tables. | IEEE abstract: 125–200 words, one paragraph, answers (1) problem/scope, (2) unique approach/contribution, (3) principal result/application. A fisheries journal specifies 200–250 words, single paragraph, no references. |
| **4. Keywords** | 5–7 terms for indexing and search; should **not** simply repeat words already in the title. | For a carp-aquaculture paper, keywords might include “Rohu, Catla, Mrigal, South Asia, floodplains, coastal zones” rather than repeating “carp” or “Bangladesh” from the title |
| **5. Introduction** | Broad context → known literature → gap → hypothesis/objectives → brief approach → sometimes a bulleted contributions list. | In computer-science conference papers, a common pattern is five paragraphs answering: What is the problem? Why is it important? Why is it hard? Why have naive approaches failed? What are the key components and results?. A contributed-paper introduction often ends with a **bulleted list of contributions**. |
| **6. Methods** | Enough detail for an independent researcher to reproduce the work; materials, participants, instruments, procedures, statistical analysis. | Elsevier: “Provide sufficient detail to allow the work to be reproduced by an independent researcher”. Established methods may be summarized and cited; new methods must be described fully |
| **7. Results** | Clear, concise findings; tables and figures; statistics; **no interpretation or literature discussion**. | Elsevier: “Results should be clear and concise … do not include references or discussion here”. A manuscript-structure guide allocates roughly **25%** of manuscript length to Results. |
| **8. Discussion** | Interpret the results; compare with prior work; explain significance, limitations, and unexpected findings; avoid overstating. | Elsevier: “Interpret your findings and compare with previous work. Address limitations and unexpected results. Avoid overstating significance”. The Research4Life framework labels Discussion as answering “What is the significance?”. |
| **9. Conclusion** | Short final takeaway; may stand alone or be a subsection of Discussion; no new data; sometimes future work. | Elsevier: conclusions “may be presented in a short Conclusions section, which may stand alone or form a subsection of a Discussion or Results and Discussion section”. Another journal template says conclusions should align with the study objectives and contain no references. |
| **10. Acknowledgements** | Funding sources, grant numbers, technical assistance, contributors who do not meet authorship criteria. | Elsevier: “Thank contributors and funders. Include grant numbers if required”. The OUP structure table lists Acknowledgements after Discussion and before References. |
| **11. References** | Full bibliographic details for every cited work, formatted in the venue’s required style; avoid excessive self-citation. | Elsevier: “Compile references; ensure accuracy and correct formatting. Avoid excessive self-citation”. The OUP structure table places References as the final major section. |

## **Short notes — structural differences by venue type**

# Citation styles (IEEE / APA / MLA / BibTeX)- one REAL example each

## **1. IEEE**

**Reference as it appears in a reference list:**

> \[1\] M. O. Hill and C. D. Preston, “Discovery of British and Irish byophytes 1. Trends in the detection and reporting of new species, 1538-2021,” _J. Bryol._, vol. 46, no. 2, pp. 79–105, Aug. 2024, doi: 10.1080/03736687.2024.2375431.

| **Element** | **Value** |
| :--- | :--- |
| **Authors** | M. O. Hill and C. D. Preston |
| **Year** | 2024 (Aug. 2024) |
| **Title** | Discovery of British and Irish byophytes 1. Trends in the detection and reporting of new species, 1538-2021 |
| **Venue** | _J. Bryol._ (abbreviated journal title) |
| **Volume** | 46 |
| **Issue** | no. 2 |
| **Pages** | 79–105 |
| **DOI** | 10.1080/03736687.2024.2375431 |

### **In-text vs. bibliography in IEEE**

|  | **In-text citation** | **Reference list** |
| :--- | :--- | :--- |
| **Form** | A **number in square brackets** (e.g., \[1\]). | A **numbered list** of full references. |
| **Ordering** | Numbers are assigned **in the order sources are first cited** in the text. | The list follows the **same citation order** — it is not alphabetical. |
| **Purpose** | The number is a pointer; the reader looks up the matching number in the list. | The list carries the full bibliographic detail needed to locate the source. |

> Example in text: _“The voltage and current discharge waveforms are uniform sine waves \[1\].”_

---

## **2. APA (7th edition)**

**Reference as it appears in a reference list:**

> Weiss, K. J., & Dube, A. R. (2016). Rational psychiatric care of jail inmates: It happened in Monterey. _Psychiatric Services_, _67_(1), 4–6. <https://doi.org/10.1176/appi.ps.201500432>

| **Element** | **Value** |
| :--- | :--- |
| **Authors** | Weiss, K. J., & Dube, A. R. |
| **Year** | 2016 |
| **Title** | Rational psychiatric care of jail inmates: It happened in Monterey |
| **Venue** | _Psychiatric Services_ (journal title and volume italicized) |
| **Volume** | 67 |
| **Issue** | (1) |
| **Pages** | 4–6 |
| **DOI** | <https://doi.org/10.1176/appi.ps.201500432> |

### **In-text vs. bibliography in APA**

|  | **In-text citation** | **Reference list** |
| :--- | :--- | :--- |
| **System** | **Author–date** citation system. | Alphabetical list of full references. |
| **Form** | Brief: author surname(s) + year, e.g., **(Weiss & Dube, 2016)** or **Weiss and Dube (2016)**. | Full entry with all publication details. |
| **Ordering** | Appears wherever the source is used in the text; order is not determined by the list. | Arranged **alphabetically by author surname**. |
| **Direct quotes** | Page number is added, e.g., **(Race, 1999, p. 55)**. | Page range appears in the full entry. |

> The in-text citation and the reference list entry must match exactly on author spelling and year.

---

## **3. MLA (9th edition)**

**Reference as it appears in a Works Cited list:**

> Akim, Rachid. “Islamophobia, Racism and the Vilification of the Muslim Diaspora.” _Islamophobia Studies Journal_, vol. 5, no. 1, 2019, pp. 26–44. _JSTOR_, <https://doi.org/10.13169/islastudj.5.1.0026>.

| **Element** | **Value** |
| :--- | :--- |
| **Author** | Akim, Rachid |
| **Year** | 2019 |
| **Title** | “Islamophobia, Racism and the Vilification of the Muslim Diaspora.” |
| **Venue** | _Islamophobia Studies Journal_ |
| **Volume** | vol. 5 |
| **Issue** | no. 1 |
| **Pages** | pp. 26–44 |
| **DOI** | <https://doi.org/10.13169/islastudj.5.1.0026> |
| **Database** | _JSTOR_ (container for the source) |

### **In-text vs. bibliography in MLA**

|  | **In-text citation** | **Works Cited** |
| :--- | :--- | :--- |
| **Form** | **Author–page** style: author surname + page number, e.g., **(Hedges 70)** or **Hedges believes … (70)**. | Full bibliographic entry. |
| **Purpose** | Brief pointer; the reader goes to Works Cited for full details. | Complete information for each source. |
| **Ordering** | Appears at the point of use; no fixed order across the paper. | **Alphabetical by author surname** (or first element if no author). |
| **No author** | Use a shortened title instead of an author name. | Entry begins with the title. |

> MLA in-text citations are also called **parenthetical citations**.

---

## **4. BibTeX**

BibTeX is **not a citation style** — it is a reference-management and database format. The “reference” is the raw entry; the rendered reference depends on the `.bst` style file chosen at compile time. Here is a real `@article` entry from ACM:

bibtex

````
@article{Abril:2007:PHD:1188913.1188915,
  author    = {Abril, Patricia S. and Plant, Robert},
  title     = {The Patent Holder's Dilemma: Buy, Sell, or Troll?},
  journal   = {Commun. ACM},
  volume    = {50},
  number    = {1},
  pages     = {36--44},
  year      = {2007},
  doi       = {10.1145/1188913.1188915},
  publisher = {ACM}
}
```[reference:18]

| Element | Value |
|---|---|
| **Authors** | Abril, Patricia S. and Plant, Robert |
| **Year** | 2007 |
| **Title** | The Patent Holder’s Dilemma: Buy, Sell, or Troll? |
| **Venue** | *Commun. ACM* (Communications of the ACM) |
| **Volume** | 50 |
| **Number (issue)** | 1 |
| **Pages** | 36–44 |
| **DOI** | 10.1145/1188913.1188915 |

### In-text vs. bibliography in BibTeX

| | In-text citation | Bibliography |
|---|---|---|
| **What it is** | A `\cite{key}` command in LaTeX. The **label** it produces depends entirely on the `.bst` style file. [reference:19] | Generated from the `.bib` database; only cited entries are listed. [reference:20] |
| **`plain` style** | **Numeric labels**, sorted alphabetically. [reference:21] | Alphabetical, numeric labels. |
| **`unsrt` style** | **Numeric labels**, but entries appear in **order of citation**. [reference:22] | Citation-order list. |
| **`alpha` style** | **Author–year labels** (e.g., `[Gui96]`). [reference:23] | Alphabetical, alphanumeric labels. |
| **Key point** | The `.bib` entry is **data**, not a formatted reference. The visible citation and the visible bibliography are both outputs of the style file applied to that data. | |

> The same `.bib` entry can render as a numeric `[1]`, an author–year `(Abril & Plant, 2007)`, or an alpha label `[AP07]`, depending on the chosen BibTeX style. [reference:24]

---

## Compact summary: in-text vs. bibliography

| Style | In-text form | Bibliography ordering | Matching rule |
|---|---|---|---|
| **IEEE** | `[1]` — number in brackets | Numbered in **citation order** | Number must match the list entry. |
| **APA** | `(Author, Year)` or `Author (Year)` | **Alphabetical** by author | Author spelling and year must match. |
| **MLA** | `(Author Page)` | **Alphabetical** by author | Author surname (or title) must match the Works Cited entry. |
| **BibTeX** | `\cite{key}` → numeric or author–year label, **depending on `.bst`** | Depends on style (`plain` = alphabetical, `unsrt` = citation order) | Citation key must exist in the `.bib` database. |

````

### **Conference papers**

- **Shorter and page-limited.** A conference paper is often **10–12 pages** (sometimes 6–12), with a strict page limit that favors a tightly scoped idea. Some fields (e.g., computer science) treat the conference paper as a “teaser” or preliminary publication.
- **Lighter review.** Conference proceedings usually receive a general readability review but are **not rigorously peer-reviewed for scientific content** in the same way as journal papers; they are seldom rejected because they report what was presented at the meeting.
- **Section emphasis.** A typical CS conference paper is organized as **Title → Abstract → Introduction → Related Work → Technical Body → Experiments → Conclusion/Future Work**. “Related Work” is often a separate section immediately after the Introduction, and “Experiments” is a first-class section.

### **Journal papers**

- **Longer and more comprehensive.** Journal papers are generally **longer** (often 20+ pages) and are allowed space to examine related work more fully, develop theoretical or algorithmic refinements, and perform a more thorough evaluation.
- **Rigorous peer review.** Journal papers are **rigorously reviewed for scientific content**; reviewers may question the validity of findings and conclusions, and papers can be rejected on scientific grounds.
- **Extension culture.** A journal paper is often an extended version of a conference paper, with **at least \~30% new material** in the extension (not just more proofs or straightforward performance numbers).

### **arXiv preprints**

- **Not peer-reviewed.** arXiv is a preprint repository; preprints are often **not peer-reviewed** and should not automatically be treated as equivalent in quality to a published journal or conference paper.
- **Flexible length and timing.** arXiv imposes **no strict page limit** in the way conferences do; a preprint can be a full technical development and is often posted **before or in parallel with** journal/conference submission.
- **Common structure.** A typical arXiv preprint in CS/ML follows: **Title → Abstract → Introduction → Related Work → Method → Experiments → Discussion/Limitations → Conclusion → References**, often using a conference style file such as NeurIPS. An arXiv LaTeX template explicitly provides `\section{Related Work}`, `\section{Method}`, and `\section{Experiments}`.

# The PDF problem (how text is stored; two-column, scanned, etc.)

## **1. How a PDF actually stores “text”**

The relevant operators (from the ISO 32000 spec) are:

| **Operator** | **Role** |
| :--- | :--- |
| `BT` / `ET` | Begin / end a text object. |
| `Tf` | Select font and size. |
| `Td` | Move the text position (translation) in user space. |
| `Tj` | Show a string of glyphs at the current position. |
| `TJ` | Show strings with per-glyph kerning adjustments. |

The ISO spec states that `Tj` “shall take a string operand and shall paint the corresponding glyphs,” and each byte in the string selects a glyph description in the font. `Td` establishes the text position on the page.

A minimal content stream looks like this:

pdf

```
BT
/F1 12 Tf
72 740 Td
(Hello) Tj
ET
```

This paints the glyphs for “Hello” at roughly x=72, y=740. **Spaces are not stored as space characters.** The gap between words is implied by a jump in the x-coordinate; the parser must infer word boundaries from font metrics.

The `TJ` operator makes this worse. It includes kerning adjustments in thousandths of a text-space unit:

pdf

```
[(A) 120 (W) 120 (A) 95 (Y)] TJ
```

Worse still, the bytes inside `Tj` are **not Unicode**. They are character codes mapped through font-specific encodings via a `CMap`. If the font includes a correct `/ToUnicode` CMap, a parser can map codes back to readable characters. If not — which happens constantly with font subsetting — the text is unrecoverable without OCR. You can copy visible text and get `(cid:38)(cid:76)(cid:81)(cid:68)(cid:81)` instead of words.

---

## **2. Why this breaks naive extraction — concrete failures**

### **Two-column layouts**

PDF provides **no internal indicator** that distinguishes two columns from a single column. A naive extractor treats the page as one wide column, effectively alternating between the two columns and merging their lines in the wrong order.

A reported Tika bug shows the failure directly: converting a two-column document produced **inverted column order**. Enabling `setSortByPosition(true)` “got scrambled” rather than fixed; copy-paste from a PDF viewer produced the correct order, but the extractor did not.

The standard workaround is to detect a narrow vertical whitespace gutter along the page’s central axis, then extract the left half before the right half. This works reasonably well — but it is easily defeated by a full-width figure or table that crosses the gutter.

### **Headers and footers**

There is **no reliable way** to distinguish running headers and footers from body text in PDF. A naive implementation will extract page numbers and chapter headings as if they were content.

Concretely, every page may inject `Chapter 3` or `42` into the middle of a paragraph if the extractor simply follows content-stream order. Detection usually relies on text density and whitespace in the upper and lower page regions — but footnotes, large images, and blank pages introduce frequent exceptions that disturb the heuristic.

### **Footnotes**

Plain-text extraction flattens the page, so **there is no obvious position for footnote text** after extraction. Distinguishing footnote text from body text is non-trivial because footnotes are denoted in many different ways. Worse, the **flags** in the main text are ambiguous: a superscripted `2` could be footnote marker 2 or an exponent in a mathematical expression — technically identical in PDF.

### **Equations**

Mathematical glyphs are often placed **one glyph at a time** at individual coordinates, especially subscripts and superscripts. A reported extraction failure shows math glyphs `x_i`, `w_i`, `Σ`, and `ϕ` coming out **scattered one-per-line**, interleaved with adjacent caption text.

Large delimiters compound the problem: a square root or a large brace may be composed of **multiple glyphs** (a radical symbol connected to a horizontal line), so a naive extractor sees disconnected pieces rather than a single mathematical object. Recovering structured math (MathML, LaTeX) requires dedicated font analysis or layout modeling, not just text extraction.

### **Ligatures**

A ligature is **two or more letters joined into a single glyph** (`ﬁ`, `ﬂ`, `ﬃ`). In extracted text they often appear as garbage Unicode characters or private-use codepoints.

A concrete example from a PDF extraction guide:

> `ﬁre` → `\u0000re`\
> `overﬂow` → `over\u0000ow`

Even though the rendered page looks perfectly fine, the extracted text is corrupted. In other PDFs, ligatures are **split into component letters with intra-word spaces**: `ﬁ` becomes `f i`, breaking word boundaries on tens of words per paper.

The root cause is missing or incomplete `/ToUnicode` mappings. When a font uses GSUB substitutions for ligatures, the ligature glyph may have **no cmap entry**, so no correct Unicode mapping is written. A parser without ligature normalization will propagate the corruption downstream.

### **Hyphenated line breaks**

PDF stores **line fragments, not words**. A word split at a line ending becomes two separate strings: `hyphen-` and `ated`.

A naive extractor typically does one of four things, none of which is universally correct:

1. **Never merge** — output `hyphen-\nated`.
1. **Always merge without a hyphen** — output `hyphenated`, which is wrong for genuine hyphenated compounds like `e-mail`.
1. **Always merge with a hyphen** — output `hyphen-ated`, which is wrong for ordinary line-breaking.
1. **Decide per case** — requires vocabulary or language-model heuristics; `ele-phant` vs `elephant` works, but `e-mail` vs `email` can be ambiguous.

---

## **3. Text PDF vs. scanned PDF**

| **Type** | **What it contains** | **Extraction result** |
| :--- | :--- | :--- |
| **Text PDF (digitally born)** | Glyph-drawing operators, embedded fonts, character codes. Text is copyable and generally error-free (subject to encoding issues). | Direct extraction works. |
| **Scanned PDF (image-only)** | A page-sized image; **no text objects**. | Text extraction returns nothing useful; OCR is required. |
| **Searchable scan** | A page image **plus an invisible OCR text layer** behind it. Fonts are present. | Extraction works, but quality depends on the OCR engine; errors are possible. |

---

## **4. How to detect each type**

**1. Count font objects (fastest screen).**\
A page that draws text must embed or reference fonts; a pure page image does not. If the PDF object graph contains **fewer than two `Font` objects**, classify as scanned. The threshold is two, not one: a single font often belongs to a scanner’s stamped label or burned-in page number, not to document text.

**2. Check for empty extraction.**\
If `extract_text()` returns nothing (or only whitespace) on a page, that page is almost certainly image-only. This is the most direct test, though it costs a full parse.

**3. Compare page count to image count.**\
If the number of pages and the number of images do not match, the PDF is likely native (not every page is a single scan). If they do match, it is _possible_ the PDF is scanned, but not guaranteed — a single page with a logo is a trivial counter-example.

**4. Compare image dimensions to the page MediaBox.**\
For each page, compare the embedded image’s width/height to the page’s MediaBox (in default user-space units, 72 dpi). If the image is larger than the page, you can infer the scan resolution. If most sampled pages yield the **same inferred DPI**, the PDF is probably a scan.

**5. Do not trust metadata or embedded-font presence alone.**\
Scanned documents can have a `Producer` field saying “Microsoft Word” . Embedded fonts can appear in scanned PDFs too, so font presence alone is not proof of a digital original. A searchable scan has fonts because of its OCR layer; a simple font-count check will call it “not scanned,” even though the page is still an image underneath.

**6. For mixed documents, classify per page.**\
A single PDF can mix native pages and scanned pages. Libraries like `pdf-inspector` return per-page types such as `"text_based"`, `"scanned"`, `"image_based"`, or `"mixed"`, and can report exactly which pages need OCR. A production pipeline should run a fast classifier first, then fall back to OCR only on pages flagged as needing it.

---

# Identifiers and metadata APIs- DOI / arXiv ID patterns and where they appear- For each API: endpoint, auth, rate limit, trimmed sample JSON

## **1. Identifier formats and where they appear**

| **Identifier** | **Official / practical pattern** | **Where it usually appears on page 1** |
| :--- | :--- | :--- |
| **DOI** | **Official structure:** `10.<registrant>/<suffix>` — directory indicator `10`, registrant code, slash, suffix. **Crossref modern-DOI regex** (case-insensitive): `^10\.\d{4,9}/[-._;()/:A-Z0-9]+$`. The literal Crossref blog pattern is `/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i`; escape the dot in production. This covers \~99.3% of Crossref DOIs, not every DOI from every registration agency. | Usually a **full URL** such as [`https://doi.org/10.1038/s41586-021-03819-2`](https://doi.org/10.1038/s41586-021-03819-2), often in the **first-page header/footer near the copyright notice or author affiliation**. Crossref recommends displaying it in full-text PDFs but does not mandate one exact coordinate. |
| **arXiv ID** | **Modern canonical:** `arXiv:YYMM.NNNNN`, with **5 sequence digits from 1501 onward**; 4 digits for 0704–1412. **Version optional:** `arXiv:YYMM.NNNNNvV`. **Legacy:** `arXiv:archive/YYMMNNN`. Practical regex: `(?i)arXiv:\d{4}\.\d{4,5}(v\d+)?` plus a legacy alternative `[a-z-]+(?:\.[A-Z]{2})?/\d{7}(v\d+)?`. | Most arXiv PDFs have an **arXiv stamp on the left-hand side of the first page**, e.g. `arXiv:0706.0001v1 [q-bio.CB] 1 Jun 2007`. This is the most reliable first-page location. |

**Extraction cautions:** DOI suffixes can contain characters outside the Crossref regex; older/other-RA DOIs may not match. arXiv IDs may be printed without the `arXiv:` prefix, and version suffixes may be omitted. Always trim trailing punctuation such as `.`, `,`, `;`, and `)`.

---

## **2. API comparison**

| **API** | **Base endpoint / single-paper lookup** | **Auth / API key** | **Rate limits** | **Licensing terms** | **What happens when the paper has no DOI** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Crossref** | [`https://api.crossref.org/works/`](https://api.crossref.org/works/)`{doi}` — e.g. `/works/10.1038/s41586-021-03819-2` | No signup required. Public pool: no auth. Polite pool: add `mailto=...` or an agent header. Metadata Plus: `Crossref-Plus-API-Token: Bearer ...`. | Public **5 req/s**, concurrency **1**; Polite **10 req/s**, concurrency **3**; Plus **150 req/s**, no concurrency limit. Exceeding returns HTTP 429. | Metadata is open; “almost none … subject to copyright,” usable for any purpose. Some abstracts may remain publisher/author copyright. | Crossref is DOI-centric; `/works/{doi}` has no key for a DOI-less paper. Use a bibliographic query such as `/works?query.bibliographic=...`, or use another source that assigns its own IDs. |
| **Semantic Scholar** | [`https://api.semanticscholar.org/graph/v1/paper/`](https://api.semanticscholar.org/graph/v1/paper/)`{paper_id}` — ID may be `DOI:...`, `ARXIV:...`, `CorpusId:...`, `PMID:...`, `URL:...`, etc. | Most endpoints work without auth. API key optional, sent as `x-api-key`; recommended for higher limits. | Unauthenticated: **1,000 req/s shared** across all anonymous users, further throttled under load. API key introductory limit: **1 req/s** across all endpoints. | API License Agreement. S2 Data is governed by accompanying licenses such as **CC BY-NC** or **ODC-BY**; attribution to “Semantic Scholar” is required. | Use another supported ID: `paperId`, `CorpusId:...`, `ARXIV:...`, `PMID:...`. DOI is simply absent from `externalIds`; the paper can still be looked up. |
| **OpenAlex** | [`https://api.openalex.org/works/`](https://api.openalex.org/works/)`{id}` — ID can be an OpenAlex `W...` ID, a DOI URL, or `doi:...`. Example: `/works/doi:10.1038/s41586-021-03819-2` | No key required for basic use. Free API key optional; send as `api_key=` query parameter or `Authorization: Bearer ...`. | No key **10 req/s**; free key or prepaid **30 req/s**; annual plan **50 req/s**. Separate daily budget applies; 429 on per-second or daily overage. | OpenAlex data is **CC0** — free to use and distribute. | Use the OpenAlex Work ID (`W...`) or another external ID. OpenAlex works can exist without a DOI; `doi` may be `null`. |
| **arXiv API** | [`http://export.arxiv.org/api/query?id`](http://export.arxiv.org/api/query?id)_`list={arxiv`_`id}` — e.g. `?id_list=1501.00001` | No auth or API key. | Legacy arXiv API: **no more than 1 request every 3 seconds**, and **one connection at a time** across all your machines. | Descriptive metadata is **CC0**. E-prints themselves remain subject to copyright; redistribution requires permission unless a permissive licence was submitted. | No DOI is needed. Lookup is by **arXiv ID**. A paper can have an arXiv ID and no DOI. If it has neither, it is not in arXiv. |

---

## **3. Trimmed sample responses**

### **Crossref — JSON**

json

```
{
  "status": "ok",
  "message": {
    "DOI": "10.1038/s41586-021-03819-2",
    "title": ["Highly accurate protein structure prediction with AlphaFold"],
    "author": [
      {"given": "John", "family": "Jumper"},
      {"given": "Richard", "family": "Evans"}
    ],
    "issued": {"date-parts": [[2021, 7, 15]]},
    "container-title": ["Nature"],
    "volume": "596",
    "page": "583-589"
  }
}
```

Crossref returns JSON. The `/works/{doi}` endpoint returns a single `message` object; an unknown DOI cannot be resolved by this endpoint.

### **Semantic Scholar — JSON**

json

```
{
  "paperId": "dc32a984b651256a8ec282be52310e6bd33d9815",
  "externalIds": {
    "PubMedCentral": "8371605",
    "DOI": "10.1038/s41586-021-03819-2",
    "CorpusId": 235959867,
    "PubMed": "34265844"
  },
  "title": "Highly accurate protein structure prediction with AlphaFold",
  "venue": "Nature",
  "year": 2021
}
```

If there is no DOI, the `"DOI"` key is simply missing; `paperId`, `CorpusId`, `PubMed`, or `ARXIV` can still identify the paper.

### **OpenAlex — JSON**

json

```
{
  "id": "https://openalex.org/W3177828909",
  "doi": "https://doi.org/10.1038/s41586-021-03819-2",
  "title": "Highly accurate protein structure prediction with AlphaFold",
  "publication_year": 2021
}
```

OpenAlex can return the same work by DOI or by its `W...` ID. For DOI-less works, `doi` may be `null`, but the `id` remains usable.

### **arXiv — Atom XML, not JSON**

xml

```
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/1501.00001v1</id>
    <title>Example arXiv paper title</title>
    <summary>Example abstract text.</summary>
    <author><name>Example Author</name></author>
    <published>2015-01-01T00:00:00Z</published>
  </entry>
</feed>
```

The arXiv API returns **Atom 1.0 XML**, not JSON. It is looked up by arXiv ID, not DOI.

---

## **4. Practical fallback chain for a PDF extractor**

1. **Try DOI first** if a plausible `10.\d{4,9}/...` string is on page 1.
1. **If DOI lookup fails or is absent**, use **arXiv ID** for arXiv API; use **Semantic Scholar** with `paperId`, `CorpusId:`, `ARXIV:`, or `PMID:`; use **OpenAlex** with its `W...` ID.
1. **If no identifier exists**, use title/author bibliographic search — but treat the result as a candidate match, not an exact lookup.
1. Never assume every paper has a DOI: Crossref is DOI-centric, while Semantic Scholar, OpenAlex, and arXiv all support non-DOI identifiers.

---

# Extraction techniques considered-> which one I chose and why

## **Comparison table (current as of October 2026)**

|  | **PyMuPDF** | **pdfplumber** | **pypdf** |
| :--- | :--- | :--- | :--- |
| **Current stable version** | **1.28.2** (2026-08-06) | **0.11.10** (2026-06-14) | **6.21.0** (2026-10-16); 6.20.1 on docs changelog |
| **License** | **AGPL-3.0** or paid commercial license from Artifex | **MIT** (permissive) | **BSD-3-Clause** (permissive) |
| **Deprecation status** | Active. `fitz` legacy import emits a warning; use `pymupdf`. | Active. No deprecation; built on `pdfminer.six`. | Active. **PyPDF2 is deprecated**; its upstream moved to `pypdf`, and PyPDF2 warns “is deprecated. Please move to the pypdf library instead.” |
| **Two-column handling** | **Best built-in support.** `get_text("blocks")` exposes block bounding boxes; `sort=True` sorts by `(y1, x0)`. Official `multi_column.py` utility detects an arbitrary number of column bounding boxes and extracts column-by-column. | **No automatic column detection.** Default `extract_text()` concatenates across the full page width, interleaving columns line-by-line. You must cluster words on `x0` / `x1` and sort manually, or use `extract_words()` and build your own reading order. | **Layout mode is visual, not logical.** `extract`_`text(extraction`_`mode="layout")` replicates the rendered layout on a fixed-width grid, but it does **not** reorder columns into reading order. Without layout mode, output follows content-stream order, which is often line-by-line across columns. |
| **Block/line granularity** | `get_text("blocks")`, `"dict"`, `"rawdict"`; block bounding boxes are first-class | Character, word, line, rectangle, and table objects; `extract_words()` returns coordinates | `visitor_text` exposes text fragments with `user_matrix` and `tm_matrix`, but no high-level block model |
| **Academic-paper fit** | **High.** Designed for complex layouts; multi-column utility; ignores headers/footers via margin parameters | **Medium.** You can achieve good results, but you must implement column detection and reading-order logic yourself. | **Low for layout.** Pure-Python, lightweight, good for metadata and simple text; not a layout engine. |

---

## **Concrete examples**

### **PyMuPDF: block extraction with reading order**

python

```
import pymupdf

doc = pymupdf.open("paper.pdf")
page = doc[0]
blocks = page.get_text("blocks")          # list of (x0, y0, x1, y1, text, block_no, block_type)
text_blocks = [b for b in blocks if b[6] == 0]  # 0 = text block

# sort=True: sorts blocks by (y1, x0) — vertical first, then horizontal
ordered = page.get_text("blocks", sort=True)
```

The `sort` parameter is documented as “sort the output by vertical, then horizontal coordinates,” which “in many cases … suffice\[s\] to generate a ‘natural’ reading order”. For reliable two-column reading, use the official `multi_column.py` utility, which detects column bounding boxes from text blocks:

python

```
from multi_column import column_boxes

for page in doc:
    bboxes = column_boxes(page, footer_margin=50)
    for bbox in bboxes:
        print(page.get_text(clip=bbox))
```

---

### **pdfplumber: manual column clustering**

python

```
import pdfplumber

with pdfplumber.open("paper.pdf") as pdf:
    page = pdf.pages[0]
    words = page.extract_words()          # each word has x0, x1, top, bottom, text

    # cluster x0 positions to find the gutter
    xs = sorted(set(round(w["x0"], 0) for w in words))
    # gap threshold ~20pt is a common starting point
    # then split words into left and right columns and sort each by top
```

The default `extract_text()` on a two-column page “returns text top-to-bottom across the entire page width,” so left and right column lines are interleaved. You must supply the reading-order logic yourself.

---

### **pypdf: layout mode preserves appearance, not semantics**

python

```
from pypdf import PdfReader

reader = PdfReader("paper.pdf")
page = reader.pages[0]
print(page.extract_text(extraction_mode="layout"))
```

This produces a fixed-width text representation that “closely adheres to the rendered layout”, but it does not infer that the left column should be read before the right. In practice, pypdf’s default mode follows content-stream order, and two-column output can alternate line-by-line between columns.

---

## **Recommendation**

**Primary recommendation: PyMuPDF — if your license permits AGPL.**

Justification:

1. **It has actual column-detection tooling.** The `multi_column.py` utility is maintained by the same project and is designed specifically for pages with a variable number of columns. No other library in this comparison ships an equivalent official utility.
1. **It exposes block geometry as a first-class API.** `get_text("blocks")` and `sort=True` give you the coordinates needed to build a reading-order model, and the blocks include type information so you can filter images and tables.
1. **It is fast.** Independent benchmarks put PyMuPDF at roughly **4.6 ms** mean extraction time per PDF vs **23.2 ms** for pdfplumber and **12.1 ms** for pypdf, with a **99.3%** pass rate on a 3,830-PDF corpus.

**If AGPL is unacceptable:** use **pdfplumber**. It is MIT-licensed, gives you character-level coordinates and table extraction, and is well suited to implementing your own column-aware reading order. Expect to write more code, and expect slower throughput.

**If you only need metadata, simple text, or a lightweight dependency:** use **pypdf**, but do **not** expect it to parse two-column academic layouts correctly out of the box. Also note that **PyPDF2 is deprecated** and should not be used for new work.

---

## 

# Tagging / topic assignment techniques-> chosen approach

## **Comparison table**

| **Technique** | **How it works** | **Strengths** | **Limits** | **Maintained Python library** |
| :--- | :--- | :--- | :--- | :--- |
| **RAKE** (Rapid Automatic Keyword Extraction) | Splits text at stopwords and punctuation into candidate phrases; scores each word by **word degree ÷ word frequency**, then sums scores within a phrase. | Unsupervised, domain-independent, very fast, no training data. | Tends to produce long candidate phrases; sensitive to the stopword list; no semantic understanding; academic text often yields generic phrases. | `rake-nltk` 1.0.6 is the most commonly used implementation, though its release cadence is slow; `python-rake` 1.5.0 is also available . |
| **YAKE** (Yet Another Keyword Extractor) | Unsupervised statistical method using **term casing, position, frequency, contextual co-occurrence, and dispersion**; single-document, no external corpus. | No training, no corpus, language- and domain-independent, works on a single abstract; actively maintained; good default for short academic text. | Purely statistical; may favor salient but generic terms; less precise than author-assigned keywords; single-document focus. | `yake` (INESCTEC), latest release 0.6.0 about six months ago; `pip install yake` . |
| **TF-IDF** | Scores terms by **term frequency × inverse document frequency**; IDF requires a **collection of documents** to estimate rarity. | Simple, interpretable, well understood; effective when a relevant local corpus exists. | **IDF is degenerate for a single paper**: if every term appears in the only document, IDF is constant or zero, so ranking collapses to term frequency. Also bag-of-words, no phrase semantics. | `scikit-learn` `TfidfVectorizer`, actively maintained . |
| **Author keywords** (parse the PDF’s own keyword section) | Locate a “Keywords”, “Key words”, or “Index Terms” block in the PDF header, then split on commas/semicolons and clean. | Highest precision when present: the authors chose the terms; no model, no corpus, no API. | **Many papers have no author keywords**, especially preprints and some fields; formatting varies; multi-line keyword blocks and hyphenation complicate parsing. GROBID’s header parser can extract keywords as structured metadata when they exist . | Custom regex/parser, or **GROBID** for robust header extraction including keywords . |
| **Controlled vocabulary matching** | Match paper text against labels and synonyms from a curated thesaurus or SKOS vocabulary (e.g. STW, MeSH-style); assign the matching concept. | Produces **normalized, consistent** labels; explainable; good for faceted search and domain-specific apps. | Coverage is limited to the vocabulary; requires curation and synonym maintenance; exact matching misses paraphrases; mapping a paper to one concept can be ambiguous. | `stwfsapy` builds a deterministic finite automaton from SKOS labels and scores matched concepts; Python ≥3.10,\<3.14 . |
| **Scholarly API topic data** (OpenAlex, Semantic Scholar) | Send title + abstract to a free API; receive normalized topics, keywords, or broad fields of study. | Zero local modelling; normalized taxonomy; OpenAlex returns fine-grained **topics and keywords** with scores; free tier available. | Not local; depends on network and rate limits; results can differ from the paper’s own terms; Semantic Scholar’s `fieldsOfStudy` is much coarser than OpenAlex topics. | **OpenAlex** `/text` endpoint and `pyalex`; **Semantic Scholar** Graph API . |

---

## **Short notes on each technique**

### **RAKE**

RAKE’s key assumption is that keywords rarely contain stopwords or punctuation, so it partitions text at those boundaries and scores the surviving phrases using word degree and frequency . It is a reasonable baseline, but on academic abstracts it often returns long, overly specific phrases. Its Python implementations are usable, but `rake-nltk` has not had a recent release, so treat it as stable-but-slow-moving rather than actively developed .

### **YAKE**

YAKE is the best **local, single-document** fallback among the three unsupervised algorithms. It requires no training corpus and no dictionaries, and it uses multiple statistical signals including casing, position, frequency, and contextual co-occurrence . For a small app that processes one paper at a time, this is a much better fit than TF-IDF, whose IDF component needs a document collection.

### **TF-IDF**

TF-IDF is often suggested for keyword extraction, but it is fundamentally a **corpus-level** weighting scheme. If your app processes one paper, every term has the same document frequency, so IDF cannot distinguish rare from common terms. TF-IDF becomes useful only if you maintain a local background corpus (e.g. 1,000 abstracts in the same field) and compute IDF against that corpus. Even then, it returns unigrams or n-grams by weight, not necessarily interpretable keyphrases.

### **Author keywords**

When a paper has a keyword block, this is the highest-precision source available. The practical challenge is **detection**: keyword sections are inconsistently labelled (“Keywords”, “Key words”, “Index Terms”), may span multiple lines, and are sometimes absent entirely. A robust option is GROBID, which parses the article header and returns keywords as structured metadata alongside title, authors, and abstract . If you want a lightweight implementation, a regex over the first page’s text looking for `(?i)^keywords?[:：]` or `index terms` is a reasonable start, but expect lower recall.

### **Controlled vocabulary matching**

This is the right choice if your app serves a **specific domain** and you already have a curated thesaurus. `stwfsapy` is a maintained library that matches SKOS thesaurus labels and synonyms to text and scores the matches . The trade-off is maintenance: a controlled vocabulary must be updated as the field evolves, and coverage gaps mean some papers receive no label. It is not a good default for a general-purpose academic paper app.

### **Scholarly API topic data**

OpenAlex’s `/text` endpoint is the most useful free option here: you send a title and optional abstract, and it returns **topics** (with subfield, field, and domain) and **keywords** from the same vocabulary used to tag indexed works . It is free with an API key (100,000 credits/day; 30 requests/second with a free key) and no key gives a much smaller testing allowance . Semantic Scholar also offers free topic-like data, but its `fieldsOfStudy` is limited to broad fields (e.g. “Computer Science”, “Medicine”) and is less useful for fine-grained keyword assignment .

---

## **Recommendation for a small app with no paid APIs**

**Use this layered pipeline:**

1. **Author keywords first.**
   - Parse the PDF header for a keyword block.
   - If present, normalize case, split on commas/semicolons, and return them directly.
   - This gives the highest precision and costs nothing.
1. **Fallback to YAKE on `title + abstract`.**
   - If no author keywords are found, run YAKE on the title and abstract only (not the full body).
   - Limit to 5–10 keyphrases.
   - This is fully local, requires no corpus, and handles multilingual papers.
   - It is the best maintained single-document extractor among RAKE, YAKE, and TF-IDF for this use case.
1. **Optional: enrich with OpenAlex `/text` if network calls are acceptable.**
   - Send `title` and `abstract` to [`https://api.openalex.org/text`](https://api.openalex.org/text).
   - Use the returned `topics` and `keywords` as normalized labels alongside the local extraction.
   - Use a free API key and cache results per DOI so you stay within the free daily budget.
   - If your app must be **fully offline**, skip this step.

**Why not TF-IDF or RAKE as the default?**

- TF-IDF needs a background corpus; for a single paper it reduces to term frequency and loses its main advantage.
- RAKE is fast but tends to produce long phrases and is more sensitive to stopword configuration; YAKE’s multiple statistical features generally make it a better single-document fallback.

**When to add controlled-vocabulary matching:**

- Only if your app serves a narrow domain and you already have a curated thesaurus.
- In that case, use `stwfsapy` as an additional normalization layer, not as the primary extractor.

---

## 

# Knowledge-graph model (nodes, edges, direction, derived edges)

## **1. Graph basics (nodes, edges, directed vs undirected)**

| **Concept** | **Meaning** | **Concrete example** |
| :--- | :--- | :--- |
| **Node / vertex** | An object in the graph. | A paper, an author, or a keyword. |
| **Edge** | A relation between two nodes. | “Paper A cites Paper B”; “Author X wrote Paper Y”. |
| **Directed** | Edge has a direction: `u → v` ≠ `v → u`. | Citation: Paper A cites Paper B, but B does not cite A. |
| **Undirected** | Edge has no direction: `u — v` is the same as `v — u`. | Co-authorship: if Alice co-authored with Bob, Bob co-authored with Alice. |

A graph can be stored as an **adjacency list** (each node keeps a list of its neighbours) or an **adjacency matrix** (an `n × n` boolean table). Relational databases naturally implement an adjacency-list-like model with an **edges table**.

---

## **2. Representing a knowledge graph in SQLite**

The canonical relational pattern is **two tables**: one for nodes, one for edges. A real-world SQLite knowledge-graph schema is deliberately small: a generic property graph with a JSON column for type-specific attributes.

sql

```
CREATE TABLE nodes (
  id         TEXT PRIMARY KEY,
  type       TEXT NOT NULL,      -- Document | Entity | Topic | Keyword ...
  props_json TEXT NOT NULL      -- free-form JSON: title, abstract, etc.
);

CREATE TABLE edges (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  rel        TEXT NOT NULL,      -- CITES | AUTHORED | ABOUT ...
  src        TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
  dst        TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
  props_json TEXT NOT NULL,
  UNIQUE (rel, src, dst)
);

CREATE INDEX idx_edges_src ON edges(src, rel);
CREATE INDEX idx_edges_dst ON edges(dst, rel);
```

This is a **property graph** in relational form: type-specific knowledge lives in `props_json`, while the structural skeleton stays generic. The `UNIQUE (rel, src, dst)` constraint prevents duplicate edges of the same relationship. Indexes on `(src, rel)` and `(dst, rel)` make one-hop traversals fast in both directions.

**Concrete query:** find all papers cited by a given paper.

sql

```
SELECT n.id, n.props_json
FROM edges e
JOIN nodes n ON n.id = e.dst
WHERE e.src = 'paper:123'
  AND e.rel = 'CITES';
```

---

## **3. Storing edges in tables vs computing them on request**

The trade-off is **read speed vs write cost and storage**.

|  | **Stored edges (materialised)** | **Computed edges (derived on request)** |
| :--- | :--- | :--- |
| **Read performance** | Fast. One indexed join or adjacency lookup. | Slower. Requires a join, aggregation, or recursive query at request time. |
| **Write cost** | Every new relation must be inserted; bulk updates can be expensive. | No edge-write cost; relations are derived from base data. |
| **Storage** | Duplicates facts already implied by base data. | No redundant storage. |
| **Consistency** | Edges can become stale unless maintained. | Always reflects the current base data. |
| **Complex traversals** | Still requires recursive CTEs in SQLite; deep or wide graphs become slow. | Same recursive cost, but repeated on every request. |

**Materialised edges behave like a materialised view.** In graph workloads, predefined joins can be materialised into extended tables and indexes, turning joins into scans and improving performance by orders of magnitude in some cases. For SQLite, a recursive CTE over an indexed edge table is the standard way to traverse a graph, but it **becomes very slow when the edge table is large** and the traversal is deep or wide. A multi-pass breadth-first approach can outperform a naive recursive CTE because it avoids re-scanning the same rows repeatedly.

**Practical rule for a small app:** store **high-value, frequently queried edges** (citations, authorship, topic assignments) as rows in `edges`. Compute **expensive transitive relationships** (e.g., “all ancestors in a citation chain”) on demand with a recursive CTE, or cache the result if the read pattern justifies it. This keeps the schema simple and avoids maintaining derived edges that are rarely used.

---

## **4. Browser graph libraries via CDN**

### **vis-network**

| **Property** | **Detail** |
| :--- | :--- |
| **Current version** | **10.1.2** |
| **License** | Apache-2.0 OR MIT |
| **jsDelivr JS URL** | [`https://cdn.jsdelivr.net/npm/vis-network@10.1.2/standalone/umd/vis-network.min.js`](https://cdn.jsdelivr.net/npm/vis-network@10.1.2/standalone/umd/vis-network.min.js) |
| **Required CSS** | **Yes.** [`https://cdn.jsdelivr.net/npm/vis-network@10.1.2/styles/vis-network.min.css`](https://cdn.jsdelivr.net/npm/vis-network@10.1.2/styles/vis-network.min.css) |
| **JSON data format** | Two arrays: `nodes` with at least `id`, and `edges` with at least `from` and `to`. |

**Concrete JSON:**

json

```
{
  "nodes": [
    {"id": 1, "label": "Paper A"},
    {"id": 2, "label": "Paper B"}
  ],
  "edges": [
    {"from": 1, "to": 2, "label": "cites"}
  ]
}
```

**CSS note:** vis-network explicitly requires its CSS file; without it, controls and layout may render incorrectly. You also typically need to size the container:

css

```
#mynetwork { width: 600px; height: 400px; }
```

### **Cytoscape.js**

| **Property** | **Detail** |
| :--- | :--- |
| **Current version** | **3.34.0** (jsDelivr package page); the GitHub repo shows a newer **3.34.4** release |
| **License** | MIT |
| **jsDelivr JS URL** | [`https://cdn.jsdelivr.net/npm/cytoscape@3.34.0/dist/cytoscape.min.js`](https://cdn.jsdelivr.net/npm/cytoscape@3.34.0/dist/cytoscape.min.js) |
| **Required CSS** | **No external CSS file from the library.** You must style the **container** (width and height), but the library’s visual styling is defined in a **JSON stylesheet**, not an external CSS file. |
| **JSON data format** | A flat `elements` array; each element has `group` (`"nodes"` or `"edges"`), `data` (with `id`, and for edges `source` and `target`), and optional `position`. |

**Concrete JSON:**

json

```
{
  "elements": [
    {"group": "nodes", "data": {"id": "a", "label": "Paper A"}},
    {"group": "nodes", "data": {"id": "b", "label": "Paper B"}},
    {"group": "edges", "data": {"id": "ab", "source": "a", "target": "b", "label": "cites"}}
  ]
}
```

**CSS note:** Cytoscape.js requires a **container element with explicit dimensions**; you must set `width` and `height` in your page’s CSS before initialisation, or layout and rendering will be incorrect. It does **not** require a library-supplied CSS file. Graph appearance is controlled by the `style` option (a JSON stylesheet) inside the `cytoscape()` call.

### **Quick comparison**

|  | **vis-network** | **Cytoscape.js** |
| :--- | :--- | :--- |
| **CDN JS** | `vis-network@10.1.2/standalone/umd/vis-network.min.js` | `cytoscape@3.34.0/dist/cytoscape.min.js` |
| **External CSS file** | **Yes** — `vis-network.min.css` | **No** — but container CSS (width/height) is required |
| **Data shape** | `{ nodes: [...], edges: [...] }` | `{ elements: [...] }` with `group` |
| **Styling model** | CSS + options object | JSON stylesheet inside the `cy` instance |
| **Best fit** | Quick network diagrams with built-in controls | Programmatic graph analysis and custom styling |

For a small app that already stores a knowledge graph in SQLite, **Cytoscape.js** avoids a second CSS dependency and gives you a first-class graph model; **vis-network** is slightly quicker to wire up visually but requires including its CSS file.

## 

# 

# Edge cases and failure modes the app must handle

## **1. Missing abstract**

**Failure mode:** Many PDFs simply do not contain an abstract, or the abstract exists in the rendered document but was never populated into any structured metadata field. In one large repository, only **8.5%** of text records had an indexed abstract; in another provider, **20%** of documents (roughly 90,000 out of 490,000) were missing an abstract from metadata. Relying on PDF metadata alone will silently drop these papers.

**Robust behaviour:**

- **Do not trust PDF metadata for abstract presence.** Attempt layout-based extraction by locating the literal heading “Abstract” and capturing the text block beneath it.
- **Fallback to the first 200–300 characters of the Introduction** as a substitute abstract when no abstract section is detected, to avoid empty fields.
- If the abstract is genuinely absent, use **automatic text summarisation** (extractive or abstractive) over the introduction or full body to generate a stand-in.
- Mark the record explicitly as `abstract`_`source: "extracted" | "fallback`_`intro" | "generated" | "missing"` so downstream consumers know the provenance.

---

### **2. Multi-line titles**

**Failure mode:** Titles are not always on one line. A simple “largest font on page 1” heuristic achieves only around **70% accuracy** under real-life conditions, and accuracies that look like 90% in papers often fall to **50–70%** when tested on real PDFs. Titles that wrap across two or three lines are easily truncated or merged with author names.

**Robust behaviour:**

- Use **font size plus spatial heuristics**: select the largest-font text block on the first page, but allow it to span **up to \~8 lines** and require it to be horizontally centred.
- Combine with **style information** (bold, colour, indentation, capitalisation) rather than font size alone.
- **Match extracted title candidates against a reference database** (Crossref, OpenAlex) using approximate string matching; this corrects multi-line and hyphenation artefacts.
- If the PDF metadata contains a title, **compare it with the layout-extracted title** and prefer the metadata title only when it is not empty and passes a plausibility check (length, no newline artefacts).

---

### **3. Many authors / affiliations**

**Failure mode:** Large author lists with superscripted affiliation markers, equal-contribution notes, and multi-affiliated researchers break simple comma-splitting. A single author can have several affiliations (primary employment, visiting position, honorary appointment), and the most common affiliation on an ORCID record is not necessarily the author’s primary appointment. Name ambiguity is also severe: the same name can refer to different people, and different spellings can refer to the same person.

**Robust behaviour:**

- **Parse the author block as structured layout**, not as plain text. Use font size, superscript markers, and line grouping to associate each affiliation marker with the correct author.
- **Resolve authors to ORCID iDs** where available. ORCID is a 16-digit alphanumeric identifier supported by major publishers (Science, Nature, PLOS, Springer, Elsevier, Wiley) and is the most reliable way to disambiguate authors across name changes and spelling variants.
- When ORCID is absent, use **affiliation-aware matching**: compare the paper’s affiliation string against the author’s known employments rather than relying on name alone. If a name match has an affiliation mismatch, flag it as ambiguous rather than silently accepting it.
- **Preserve the raw author string** alongside the structured representation; do not discard the original text when normalisation fails.

---

### **4. Non-English text (CJK, RTL, Cyrillic, Thai, etc.)**

**Failure mode:** PDFs do not guarantee a correct mapping from glyph codes to Unicode. Multilingual extraction is substantially harder: models that work well on Latin-script languages show an average **14% performance drop** on non-Latin scripts, and accuracy on Arabic and Hindi can fall **below 10%**. Specific failures include dropping vowel diacritics in Hindi, confusing visually identical Cyrillic and Latin characters, hallucinating spaces in Thai, and processing right-to-left Arabic columns in left-to-right order. Bidirectional text (mixed LTR/RTL) requires applying the Unicode BIDI algorithm to convert presentation order back to logical order.

**Robust behaviour:**

- **Detect the script and language** before extraction. Do not apply English-only heuristics (stopword lists, hyphenation rules, title casing) to non-Latin text.
- For **RTL scripts**, use a PDF library with full Unicode and BIDI support (e.g., PDFBox with ICU4J) rather than reversing character order manually; naive reversal produces disordered words.
- For **CJK**, account for different writing directions and avoid assuming spaces delimit words.
- If the extracted text is below a plausible length threshold or contains excessive replacement characters (`\ufffd`), **flag the page for OCR** with a multilingual model rather than accepting the garbled output.

---

### **5. No DOI**

**Failure mode:** A paper without a DOI is not retrievable by any DOI-keyed endpoint. OpenAlex explicitly states that title-and-author matching is the fallback when no DOI is available. In OpenCitations, roughly **1.4%** of graph rows carry an OpenAlex ID and no DOI. Rejecting DOI-less papers loses legitimate literature.

**Robust behaviour:**

- **Try alternative identifiers in order:** arXiv ID (including the DataCite DOI `10.48550/arXiv.YYMM.NNNNN`), PubMed ID (PMID), PubMed Central ID (PMCID), OpenAlex work ID (`W...`), and Semantic Scholar `paperId` or `CorpusId`.
- **Fall back to bibliographic matching** on normalised title and first-author surname. OpenAlex recommends using `<dc:title>` and `<dc:creator>` for this fallback.
- **Cache by a canonical internal ID**, not by DOI. OpenAlex work IDs and arXiv IDs can serve as first-class keys; a PMID can be traded for a DOI on first use but should not become a second cache key.
- **Never silently drop a DOI-less paper.** Store it with `doi: null` and the best available alternative identifier.

---

### **6. Scanned pages**

**Failure mode:** A scanned PDF contains page images with no usable text operators. A naive extractor returns empty strings or garbage. Mixed documents are common: some pages are born-digital, others are scans.

**Robust behaviour:**

- **Detect scans per page, not per document.** Flag a page as scanned when it has **little extractable text** or when **embedded images cover ≥ 50% of the page**. The second rule catches “scan-strip” PDFs where each page is a scan tiled into thin image strips with a baked-in OCR layer that is unreliable.
- **Route scanned pages to OCR** (e.g., PaddleOCR with an EasyOCR fallback) and **born-digital pages to layout-based extraction**. Do not OCR a page that already has clean text; OCR introduces errors.
- For layout-heavy scans, run **layout analysis** (PP-Structure or equivalent) to recover figure, table, and text regions, not just raw character strings.
- Treat OCR output as lower-confidence: keep the page image alongside the extracted text for auditability.

---

### **7. References split across columns**

**Failure mode:** PDF provides no internal indicator that distinguishes two columns from one wide column. A naive extractor treats a two-column page as a single column and **alternates line-by-line between the left and right columns**, merging unrelated text. Reference lists are especially vulnerable because they are dense, often have hanging indents, and may be interrupted by footnotes or full-width tables.

**Robust behaviour:**

- **Detect a central vertical gutter** of whitespace and extract the left half before the right half. This works for simple two-column layouts but is defeated by full-width elements that cross the gutter.
- Use a **layout-aware parser** that groups text into regions (body, footnote, reference list) before sequencing those regions, rather than sorting raw coordinates.
- **Consolidate footnotes and rejoin reference entries** that were split by column or page boundaries. Reference strings may continue across pages with no visual marker.
- **Validate the reference section against Crossref or OpenAlex** after extraction. Resolving each parsed reference to a DOI provides a strong signal that the split was repaired correctly; unresolved references can be flagged for manual review.

---

### **8. Duplicate uploads**

**Failure mode:** The same paper can be uploaded multiple times: the published version, a preprint, a repository copy, and a reformatted PDF. Byte-identical hashing catches only exact duplicates; near-duplicates (different stylesheet, different pagination, different OCR layer) pass through.

**Robust behaviour:**

- **Hash the normalised text**, not the file bytes. Extract text, strip whitespace and punctuation, then compute a **SimHash** fingerprint. SimHash provides fast near-duplicate detection with a formal probabilistic guarantee, though it is insensitive to word order and semantic paraphrase.
- **Confirm candidates with a stricter similarity measure.** A two-stage pipeline using SimHash followed by **Smith-Waterman text alignment** at a selected similarity threshold reduces the false-positive rate to **near zero** without lowering sensitivity.
- **Deduplicate by canonical identifier first** (DOI, arXiv ID, PMID, OpenAlex ID). Only fall back to content similarity when no identifier is available or when identifiers differ but the text is suspiciously similar.
- Store the duplicate relationship explicitly (`duplicate`_`of: canonical`_`id`) rather than discarding the second upload; the alternate version may contain corrections or supplementary material.

---

### **9. Malformed references**

**Failure mode:** Reference strings are highly variable. GROBID’s default model is tuned for structured scientific bibliographies and performs poorly on **footnote-based citation styles**: precision is high (0.89–0.94) but recall is extremely low (0.21–0.27), because most footnote citations are never recognised as bibliographic content. Even when a reference is detected, field extraction can fail: dates may be inline, abbreviated, or interleaved with volume numbers.

**Robust behaviour:**

- **Do not rely on a single parser.** GROBID is strong and fast on well-structured PDFs, but LLMs are more robust against multilingual and non-standard formatting. Use GROBID as the primary parser and an LLM (or a domain-specialised model) as a fallback when the parsed reference is empty or fails schema validation.

- **Validate parsed references against a structured schema** (authors, title, year, venue, identifiers). If the output is malformed or empty, perform a **single retry** with identical settings, then count the reference as a failure rather than silently emitting partial data.

- **Resolve references against Crossref or OpenAlex** to confirm the parse. A reference that resolves to a real DOI is strong evidence that the parse is correct; unresolved references should be flagged as low-confidence.

- **Preserve the raw reference string** alongside the parsed fields. When parsing fails, the raw string is still searchable and can be repaired later without re-extracting the PDF.

- Graph definition, directed vs undirected: **Taylor & Francis, “Graphs”** — [`https://www.taylorfrancis.com/chapters/mono/10.1201/9781420035179-12/graphs-dinesh-mehta-dinesh-mehta-sartaj-sahni`](https://www.taylorfrancis.com/chapters/mono/10.1201/9781420035179-12/graphs-dinesh-mehta-dinesh-mehta-sartaj-sahni)

- Directed vs undirected edge semantics, adjacency matrix: **CMU 15-121, “Graphs”** — [`https://www.cs.cmu.edu/~tcortina/15-121sp10/Unit09.pdf`](https://www.cs.cmu.edu/\~tcortina/15-121sp10/Unit09.pdf)

- SQLite knowledge-graph schema (`nodes`, `edges`, JSON props, indexes): **ragraph `graph-schema.md`** — [`https://github.com/ADVASYS/ragraph/blob/main/docs/graph-schema.md`](https://github.com/ADVASYS/ragraph/blob/main/docs/graph-schema.md)

- Materialised graph joins vs computed joins, order-of-magnitude gains: **ACM, “Making RDBMSs efficient on graph workloads”** — [`https://dl.acm.org/doi/pdf/10.1145/3472163.3472269`](https://dl.acm.org/doi/pdf/10.1145/3472163.3472269)

- SQLite recursive CTE performance degradation on large edge tables: **Stack Overflow, “Efficient paths in directed graph with SQL”** — [`https://stackoverflow.com/questions/75580234/`](https://stackoverflow.com/questions/75580234/)

- vis-network version, license, jsDelivr URL, CSS URL: **jsDelivr vis-network package page** — [`https://www.jsdelivr.com/package/npm/vis-network`](https://www.jsdelivr.com/package/npm/vis-network)

- vis-network data format (`nodes`/`edges` with `id`/`from`/`to`) and CSS requirement: **vis-network basic usage** — [`https://visjs.github.io/vis-network/examples/network/basic_usage/legacy.html`](https://visjs.github.io/vis-network/examples/network/basic_usage/legacy.html); **vis.js network documentation** — [`https://visjs.github.io/vis-network/docs/network/`](https://visjs.github.io/vis-network/docs/network/)

- Cytoscape.js version, license, jsDelivr package: **jsDelivr cytoscape package page** — [`https://www.jsdelivr.com/package/npm/cytoscape`](https://www.jsdelivr.com/package/npm/cytoscape); GitHub releases — [`https://github.com/cytoscape/cytoscape.js`](https://github.com/cytoscape/cytoscape.js)

- Cytoscape.js `elements` format, container CSS requirement, JSON stylesheet: **Cytoscape.js getting started** — [`https://github.com/cytoscape/cytoscape.js/blob/.../documentation/md/getting-started.md`](https://github.com/cytoscape/cytoscape.js/blob/.../documentation/md/getting-started.md); **Cytoscape manual, Cytoscape.js section** — [`https://manual.cytoscape.org/en/3.7.1/Cytoscape.js`](https://manual.cytoscape.org/en/3.7.1/Cytoscape.js)_`and`_`Cytoscape.html`

- RAKE algorithm and scoring (word degree, frequency, stopword partitioning): [`https://pmc.ncbi.nlm.nih.gov/articles/PMC9753895/`](https://pmc.ncbi.nlm.nih.gov/articles/PMC9753895/)

- `rake-nltk` package and maintenance status: [`https://pypi.org/project/rake-nltk/`](https://pypi.org/project/rake-nltk/) and [`https://pypi.org/project/python-rake/`](https://pypi.org/project/python-rake/)

- YAKE official repository and features: [`https://github.com/INESCTEC/yake`](https://github.com/INESCTEC/yake)

- YAKE statistical features (casing, position, frequency, co-occurrence): [`https://github.com/LIAAD/yake_demo`](https://github.com/LIAAD/yake_demo) and [`https://pmc.ncbi.nlm.nih.gov/articles/PMC9753895/`](https://pmc.ncbi.nlm.nih.gov/articles/PMC9753895/)

- scikit-learn `TfidfVectorizer`: [`https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

- GROBID header extraction, including keywords: [`https://grobid.readthedocs.io/en/latest/Introduction/`](https://grobid.readthedocs.io/en/latest/Introduction/)

- `stwfsapy` controlled-vocabulary matching: [`https://pypi.org/project/stwfsapy/`](https://pypi.org/project/stwfsapy/)

- OpenAlex `/text` endpoint for topics and keywords: [`https://help.openalex.org/api/tag-aboutness`](https://help.openalex.org/api/tag-aboutness)

- OpenAlex authentication and rate limits: [`https://help.openalex.org/api/authentication/`](https://help.openalex.org/api/authentication/)

- `pyalex` Python client for OpenAlex: [`https://pypi.org/project/pyalex/`](https://pypi.org/project/pyalex/)

- Semantic Scholar API and fields of study: [`https://www.semanticscholar.org/product/api`](https://www.semanticscholar.org/product/api) and [`https://development.semanticscholar.org/`](https://development.semanticscholar.org/)

- Author keyword absence in many papers: [`https://www.ideals.illinois.edu/items/...`](https://www.ideals.illinois.edu/items/...) (study reporting a large portion of papers with no keyword or only one keyword)

- PyMuPDF changelog and version 1.28.2: [`https://pymupdf.readthedocs.io/en/latest/changes.html`](https://pymupdf.readthedocs.io/en/latest/changes.html)

- PyMuPDF licensing (AGPL / commercial): [`https://pymupdf.io/licensing`](https://pymupdf.io/licensing) and [`https://pypi.org/project/pymupdf/`](https://pypi.org/project/pymupdf/)

- PyMuPDF text extraction details, `sort` parameter, block coordinates: [`https://pymupdf.readthedocs.io/en/latest/appendix1.html`](https://pymupdf.readthedocs.io/en/latest/appendix1.html) and [`https://pymupdf.readthedocs.io/en/latest/textpage.html`](https://pymupdf.readthedocs.io/en/latest/textpage.html)

- Artifex blog, “Extract Text From a Multi-Column Document Using PyMuPDF in Python”: [`https://artifex.com/blog/extract-text-from-a-multi-column-document-using-pymupdf-in-python`](https://artifex.com/blog/extract-text-from-a-multi-column-document-using-pymupdf-in-python)

- pdfplumber changelog and version 0.11.10: [`https://github.com/jsvine/pdfplumber/blob/stable/CHANGELOG.md`](https://github.com/jsvine/pdfplumber/blob/stable/CHANGELOG.md)

- pdfplumber license (MIT): [`https://pypi.org/project/pdfplumber/`](https://pypi.org/project/pdfplumber/)

- pdfplumber multi-column limitation (default interleaving): [`https://theneuralbase.com/pdf-processing/learn/advanced/multi-column-layout-handling/`](https://theneuralbase.com/pdf-processing/learn/advanced/multi-column-layout-handling/)

- pypdf changelog and version 6.21.0: [`https://pypdf.readthedocs.io/en/6.20.1/meta/CHANGELOG.html`](https://pypdf.readthedocs.io/en/6.20.1/meta/CHANGELOG.html)

- pypdf license (BSD-3-Clause): [`https://pypdf.readthedocs.io/en/stable/faq.html`](https://pypdf.readthedocs.io/en/stable/faq.html)

- pypdf layout-mode documentation: [`https://pypdf.readthedocs.io/en/4.2.0/user/extract-text.html`](https://pypdf.readthedocs.io/en/4.2.0/user/extract-text.html)

- PyPDF2 deprecation notice: [`https://pypi.org/project/obelize/`](https://pypi.org/project/obelize/) (PyPDF2 warns “is deprecated. Please move to the pypdf library instead.”)

- Performance and license comparison: [`https://pdf.oxide.fyi/java/docs/comparison/python`](https://pdf.oxide.fyi/java/docs/comparison/python)

- DOI structure and prefix/suffix rules: DOI Handbook / DOI syntax summaries — [`https://www.doi.org/doi`](https://www.doi.org/doi)_`handbook/2`_`Numbering.html#2.2`

- Crossref modern-DOI regex and caveats: [`https://www.crossref.org/blog/dois-and-matching-regular-expressions/`](https://www.crossref.org/blog/dois-and-matching-regular-expressions/)

- Crossref DOI display guidance, including full-text PDFs: [`https://www.crossref.org/display-guidelines/`](https://www.crossref.org/display-guidelines/)

- arXiv identifier format, version suffix, and PDF left-margin stamp: [`https://info.arxiv.org/help/arxiv_identifier.html`](https://info.arxiv.org/help/arxiv_identifier.html)

- arXiv API manual, base URL, Atom XML response: [`https://info.arxiv.org/help/api/user-manual.html`](https://info.arxiv.org/help/api/user-manual.html)

- arXiv API Terms of Use, rate limits, metadata CC0, copyright: [`https://info.arxiv.org/help/api/tou.html`](https://info.arxiv.org/help/api/tou.html)

- Crossref REST API endpoints and open metadata: [`https://www.crossref.org/documentation/retrieve-metadata/rest-api/`](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

- Crossref access pools and exact rate/concurrency limits: [`https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/`](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/)

- Semantic Scholar API overview and rate limits: [`https://www.semanticscholar.org/product/api`](https://www.semanticscholar.org/product/api)

- Semantic Scholar API tutorial and paper endpoint: [`https://www.semanticscholar.org/product/api/tutorial`](https://www.semanticscholar.org/product/api/tutorial)

- Semantic Scholar API reference and sample `externalIds`: [`https://api.semanticscholar.org/api-docs/`](https://api.semanticscholar.org/api-docs/)

- Semantic Scholar API License Agreement: [`https://www.semanticscholar.org/product/api/license`](https://www.semanticscholar.org/product/api/license)

- OpenAlex authentication and per-second rate limits: [`https://help.openalex.org/api/authentication/#rate-limits`](https://help.openalex.org/api/authentication/#rate-limits)

- OpenAlex endpoints and single-work lookup: [`https://help.openalex.org/api/endpoints/`](https://help.openalex.org/api/endpoints/)

- OpenAlex Works overview: [`https://help.openalex.org/api/works`](https://help.openalex.org/api/works)

- OpenAlex CC0 licensing FAQ: [`https://ourresearch.gitbook.io/help.openalex.org/faq`](https://ourresearch.gitbook.io/help.openalex.org/faq)

- **S1** — LlamaIndex, “Why Reading PDFs is Hard” (2026): [`https://www.llamaindex.ai/blog/why-reading-pdfs-is-hard`](https://www.llamaindex.ai/blog/why-reading-pdfs-is-hard)

- **S2** — ISO 32000 (PDF spec), glyph painting, `Tf`, `Td`, `Tj`, `TJ`: [`https://archive.org/download/ISODIS32000E/ISO`](https://archive.org/download/ISODIS32000E/ISO)_`DIS`_`32000_(E).pdf`

- **S3** — FOI report, “Page headers and footers… two columns… footnotes”: [`https://www.foi.se/rest-api/report/FOI-R--5544--SE`](https://www.foi.se/rest-api/report/FOI-R--5544--SE)

- **S4** — Apache Tika issue TIKA-1533, “PDF parse failing to capture right order of text (2 columns)”: [`https://issues.apache.org/jira/si/jira.issueviews:issue-html/TIKA-1533/TIKA-1533.html`](https://issues.apache.org/jira/si/jira.issueviews:issue-html/TIKA-1533/TIKA-1533.html)

- **S5** — Sensible, “Ligatures” (PDF extraction): [`https://docs.sensible.so/docs/ligatures`](https://docs.sensible.so/docs/ligatures)

- **S6** — pdf_oxide issue #551, “Latin ligatures … split into component letters with intra-word spaces”: [`https://github.com/yfedoseev/pdf_oxide/issues/551`](https://github.com/yfedoseev/pdf_oxide/issues/551)

- **S7** — pdf_oxide issue #556, “figure-region math glyphs … emitted line-per-glyph”: [`https://github.com/yfedoseev/pdf_oxide/issues/556`](https://github.com/yfedoseev/pdf_oxide/issues/556)

- **S8** — “Improved Dehyphenation of Line Breaks for PDF Text Extraction” (Freiburg thesis): [`https://ad-publications.cs.uni-freiburg.de/theses/Bachelor`](https://ad-publications.cs.uni-freiburg.de/theses/Bachelor)_`Mari`_`Hernaes`_`2019`_`presentation.pdf`

- **S9** — PDFlib TET, dehyphenation behavior: [`https://www.pdflib.com/products/tet/features/`](https://www.pdflib.com/products/tet/features/)

- **S10** — Unidoc, “Detect Scanned PDF Document” (font-object threshold): [`https://docs.unidoc.io/unipdf/guides/analysis/detect-scanned-pdf-document/`](https://docs.unidoc.io/unipdf/guides/analysis/detect-scanned-pdf-document/)

- **S11** — Open Preservation Foundation, “Scanned vs native PDFs, how to differentiate them?”: [`https://openpreservation.org/blogs/scanned-vs-native-pdfs-how-to-differentiate-them/`](https://openpreservation.org/blogs/scanned-vs-native-pdfs-how-to-differentiate-them/)

- **S12** — Stack Overflow, “How can I distinguish a digitally-created PDF from a searchable PDF?”: [`https://stackoverflow.com/questions/63494812/`](https://stackoverflow.com/questions/63494812/)

- **S13** — `pdf-inspector` (per-page type classification): [`https://pypi.org/project/pdf-inspector/`](https://pypi.org/project/pdf-inspector/)

- **S14** — RIT, “Extraction of Math Expressions from PDF Documents” (multi-glyph delimiters): [`https://cs.rit.edu/~rlaz/files/mathPDF.pdf`](https://cs.rit.edu/\~rlaz/files/mathPDF.pdf)

- **S15** — ScholarPhi, math extraction from PDFs: [`https://export.arxiv.org/abs/2108.06337`](https://export.arxiv.org/abs/2108.06337)

# what I discarded and why

" A PDF page is a sequence of **drawing operators** in a content stream. There are no `<p>`, `<h1>`, or `<column>` tags. What looks like a sentence is a series of commands that place glyph shapes at coordinates."

" A parser has to decide whether each numeric gap is kerning (within a word) or a word boundary. There is no definitive answer — it depends on the font and the PDF generator."

"The PDF spec _does_ define a “Tagged PDF” mode with structural primitives, but the vast majority of real-world PDFs contain none of it. A table, for example, is just grid lines drawn with path operators plus cell text placed at coordinates — there is no semantic connection between the lines and the text."

"Dehyphenation is not the default in many libraries; PDFlib, for example, only combines hyphenated word parts when dehyphenation is explicitly enabled."

why? - Generic Explanations and Definitions

&#32;

# Sources

**PDF Parsing & Extraction**

1. <https://arxiv.org/abs/2010.12647> — How PDFs store text as coordinate-based glyphs; multi-column detection logic.
1. <https://arxiv.org/abs/2410.09871> — Comparative study: PyMuPDF/pypdfium best for text, but struggle with scientific docs.
1. <https://github.com/> — Practical PyMuPDF vs. pdfplumber vs. pypdf trade-offs (search "PDF extraction guide").
1. <https://blog.filestack.com/extract-text-from-pdf-python/> — PyMuPDF AGPL license note and speed comparison.

**Metadata APIs (DOI, Crossref, OpenAlex, arXiv)**

1. <https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/> — Public (5/s) vs. Polite (10/s) rate limits; `mailto` parameter.
1. <https://help.openalex.org/api/authentication> — Free API key gives $1/day, 30 req/s.
1. <https://info.arxiv.org/help/api/user-manual.html> — Atom XML response format and query parameters.
1. <https://www.doi.org/the-identifier/what-is-a-doi/> — DOI syntax: `10.` prefix + suffix structure.
1. <https://api.semanticscholar.org/api-docs/> — Semantic Scholar API rate limits and response fields.

**Citation Styles (IEEE, APA, MLA, BibTeX)**

1. <https://www.degruyter.com/document/doi/10.1515/9783110613247-006/pdf> — Real IEEE example with DOI.
1. <https://apastyle.apa.org/style-grammar-guidelines/references/examples/journal-article-references> — Real APA example with DOI.
1. <https://langara.libguides.com/c.php?g=1040804&p=7541208> — Real MLA example with DOI.
1. <https://netlib.sandia.gov/bibnet/faqA.html> — Real BibTeX entry syntax.

**Knowledge Graph Libraries**

1. <https://visjs.github.io/vis-network/examples/> — vis-network nodes/edges JSON format.
1. <https://js.cytoscape.org/> — Cytoscape.js CDN loading note and data format.

**Tagging & Keyword Extraction**

1. <https://github.com/LIAAD/yake> — YAKE keyword extraction library documentation.
1. <https://github.com/anespinosa/rake-nltk> — RAKE keyword extraction library documentation.

**Python Web Frameworks & SQLite**

1. <https://flask.palletsprojects.com/en/3.0.x/> — Flask documentation (for serving static files and handling uploads).
1. <https://docs.python.org/3/library/sqlite3.html> — Python `sqlite3` standard library documentation.

**General Academic Metadata / OpenAlex**

1. <https://docs.openalex.org/> — OpenAlex API documentation.

# SAMPLES AS EXAMPLES

## SAMPLE 1: CHARTS AS EPISTEMIC ACTIONS FOR EXPERIENCEDRIVEN AGENTIC DATA ANALYSIS 

### Excerpt

"Data agents built on ReAct-style loops now execute complex analytical workflows over structured data, yet their intermediate reasoning still runs almost entirely through text. Human analysts instead move between numbers, tables, and charts, reading visual evidence to expose trends and anomalies that text summaries drop. We ask whether charts can serve as internal epistemic actions inside a data agent’s reasoning loop, and how to teach an agent to use them. We first build PROBEBENCH, a suite of 200 controlled tasks under four matched interface conditions, and find a persistent gap between what agents can read and what they choose to use."

### Report:

Extracted Sections

- **Title:** CHARTS AS EPISTEMIC ACTIONS FOR EXPERIENCE-DRIVEN AGENTIC DATA ANALYSIS
- **Author List:** Xinzhe Wang¹, Xudong Weng¹, Zang Li, Shaolei Zhang² (Tencent, Renmin University of China)
- **Abstract:** Data agents built on ReAct-style loops now execute complex analytical workflows over structured data, yet their intermediate reasoning still runs almost entirely through text. Human analysts instead move between numbers, tables, and charts, reading visual evidence to expose trends and anomalies that text summaries drop. We ask whether charts can serve as internal epistemic actions inside a data agent's reasoning loop, and how to teach an agent to use them. We first build PROBEBENCH, a suite of 200 controlled tasks under four matched interface conditions, and find a persistent gap between what agents can read and what they choose to use. Agents score as well from self-generated charts as from numeric output, yet plotting access alone does not translate into consistent use. Task slices show that charts lead on temporal, pattern, and anomaly reasoning, while text leads on precise reading and conditional verification. We then propose CHARTMIND, which distils two families of experience from conditioned trajectory rollouts. One family records how to select and verify analytical operations, and the other records when to invoke text, charts, or both. A trajectory judge scores outcomes and labels intermediate steps, and a validation gate admits only experience that improves held-out performance. On three held-out benchmarks with four LLM backbones, CHARTMIND raises analytical accuracy and visual evidence quality over matched baselines, and backbones that never drew charts begin using them, all without touching model parameters.
- **Reference Section:**
  > **REFERENCES**
  >
  > Jason Brown. An introduction to the bootstrap. _Journal of Quality Technology_, 27(1):90–91, 1995. doi: 10.1080/00224065.1995.11979565. URL <https://doi.org/10.1080/00224065.1995.11979565>.
  >
  > Amit Kumar Das, Mohammad Tarun, and Klaus Mueller. Charts-of-thought: Enhancing LLM visualization literacy through structured data extraction. _IEEE Transactions on Visualization and Computer Graphics_, 32(1):1427–1437, 2026. doi: 10.1109/TVCG.2025.3634813. URL <https://doi.org/10.1109/TVCG.2025.3634813>.
  >
  > Victor Dibia. LIDA: A tool for automatic generation of grammar-agnostic visualizations and infographics using large language models. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)_, pp. 113–126. Association for Computational Linguistics, 2023. doi: 10.18653/v1/2023.acl-demo.11. URL <https://aclanthology.org/2023.acl-demo.11/>.
  >
  > _(... 27 entries total, spanning pages 10–12)_\[cite: 10, 11, 12\]

Layout, Formatting, and Formatting Patterns

- **DOI Appearance & Position:**
  - **Page & Location:** Appears on Page 1 in the top-left header region as an arXiv identifier. Individual paper DOIs appear in the Reference section (Pages 10–12) at the end of each cited item\[cite: 10, 11, 12\].

  - **Format:** Formatted as `arXiv:2610.30072v1 [cs.AI] 21 Oct 2026` at the top header, and as standard `doi: 10.xxxx/...` inside the references\[cite: 10, 11, 12\].

  - **Excerpt:**

    Plaintext

    ```
    arXiv:2610.30072v1 [cs.AI] 21 Oct 2026
    
    ```

    Plaintext

    ```
    doi: 10.1080/00224065.1995.11979565.
    
    ```
- **Reference Section Start:**
  - Starts at the top of Page 10 under a centered/left-aligned uppercase heading titled `REFERENCES` in bold.

  - **Excerpt:**

    Plaintext

    ```
    REFERENCES
    Jason Brown. An introduction to the bootstrap...
    
    ```
- **Reference Numbering & Formatting:**
  - **Formatting Style:** Formatted in unnumbered, alphabetical order by the first author's last name. Uses hanging indents. In-text citations use author-year format, such as `(Yao et al., 2023)` or `(Brown, 1995)`\[cite: 2\].

  - **Excerpt:**

    Plaintext

    ```
    Jason Brown. An introduction to the bootstrap. Journal of Quality Technology, 27(1):90-91, 1995.
    
    ```
- **Layout Quirks:**
  - **Single-Column Layout:** The document is strictly single-column throughout.
  - **Section Headers & Appendices:** Uses bold numbered section headers (e.g., `1 INTRODUCTION`, `2 CHARTS IN THE ANALYTICAL LOOP`)\[cite: 1, 2\]. Appendices (`A TOKEN COST`, `B IMPLEMENTATION DETAILS...`) are lettered and positioned after the reference section\[cite: 13, 14\].
  - **System Prompts / Code Snippets:** Extensive verbatim prompt blocks and system messages are placed in shaded gray boxes in Appendix B\[cite: 14, 15, 16\].

&#32; 

## SAMPLE 2: TIDE: Tree-Induced Fine-Grained Diagnostic Evaluation from Model Behaviors

### Excerpt

"Benchmark performance is the dominant standard for comparing large language models (LLMs), typically summarized by a single aggregate score, such as accuracy, pass rate, or rubric score. This aggregate score provides limited information about a model’s underlying capabilities, yet understanding these capabilities is crucial for model development and evaluation. To this end, we propose Tree-Induced Diagnostic Evaluation (TIDE), which recasts diagnostic evaluation as behavior driven decision-tree induction to perform fine-grained capability diagnosis."

### Report:

Extracted Sections

- **Title:** TIDE: Tree-Induced Fine-Grained Diagnostic Evaluation from Model Behaviors\[cite: 24\]
- **Author List:** Jiayi Chen¹,², Hui Li¹_, Yujiong Shen¹,²_, Qiyuan Peng¹, Yanxin Li¹, Chenhao Huang¹,², Shaofan Liu¹,², Guoqiang Zhang¹, Junjie Ye¹,², Shihan Dou¹,², Ming Zhang¹,², Maxm Pan², Tao Gui¹†, Qi Zhang¹, Xuanjing Huang¹ (Fudan University, Hunyuan Team, Tencent)\[cite: 24\]
- **Abstract:** Benchmark performance is the dominant standard for comparing large language models (LLMs), typically summarized by a single aggregate score, such as accuracy, pass rate, or rubric score. This aggregate score provides limited information about a model's underlying capabilities, yet understanding these capabilities is crucial for model development and evaluation. To this end, we propose Tree-Induced Diagnostic Evaluation (TIDE), which recasts diagnostic evaluation as behavior-driven decision-tree induction to perform fine-grained capability diagnosis. TIDE recursively builds a hierarchical capability tree from benchmark samples and model scores: at each node, an LLM judge proposes candidate splits and performs sample-to-group classification, and behavior-based information gain selects among them. We apply TIDE to five models across four benchmarks to demonstrate its effectiveness, and find fine-grained capability contrasts invisible at the aggregate level: Claude Opus 4.6 achieves 100% on microeconomic market reasoning where GPT-5.4 scores 83.3%, but trails GPT-5.4 on contract law reasoning with 77.8% versus 88.9%. We hope TIDE can be extended to past and future benchmarks so that the rich behavioral signal in evaluation results is fully leveraged for understanding model capabilities.\[cite: 24\]
- **Reference Section:**
  > **References**\[cite: 34\]
  >
  > Lorin W Anderson and David R Krathwohl. A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives: complete edition. Addison Wesley Longman, Inc., 2001.\[cite: 34\]
  >
  > Anthropic. Claude opus 4.6 model card. Technical report, 2025. URL <https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf>.\[cite: 34\]
  >
  > Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. arXiv preprint arXiv:2309.16609, 2023.\[cite: 34\]
  >
  > _(... 43 entries total, spanning pages 11–14)_\[cite: 34, 35, 36, 37\]

Layout, Formatting, and Formatting Patterns

- **DOI Appearance & Position:**
  - **Page & Location:** Top left header of Page 1 contains the arXiv submission indicator\[cite: 24\]. DOIs/URLs appear inside reference entries\[cite: 34, 35\].

  - **Format:** `arXiv:2610.29985v1 [cs.AI] 21 Oct 2026` in the header\[cite: 24\].

  - **Excerpt:**

    Plaintext

    ```
    arXiv:2610.29985v1 [cs.AI] 21 Oct 2026
    
    ```
- **Reference Section Start:**
  - Located on Page 11 following Section 6 (Conclusion) and Limitations, headed by `References` in bold\[cite: 33, 34\].

  - **Excerpt:**

    Plaintext

    ```
    References
    Lorin W Anderson and David R Krathwohl...
    
    ```
- **Reference Numbering & Formatting:**
  - **Formatting Style:** Unnumbered, sorted alphabetically by primary author's surname with hanging indents\[cite: 34\]. In-text citations use parenthetical author-year style (e.g., `(Breiman et al., 2017; Quinlan, 1986)`)\[cite: 25, 26\].

  - **Excerpt:**

    Plaintext

    ```
    Leo Breiman, Jerome Friedman, Richard A Olshen, and Charles J Stone. Classification and regression trees. Chapman and Hall/CRC, 2017.
    
    ```
- **Layout Quirks:**
  - **Many Authors:** Features an extensive 18-author list with complex footnote annotations for equal contribution (`*`) and corresponding authors (`†`)\[cite: 24\].
  - **Wide Full-Page Tables:** Appendices contain large landscape/full-width node description tables (e.g., Table 4, Table 6) detailing decision tree branches\[cite: 50, 51, 52, 57, 58\].
  - **Algorithm Box:** Includes a formal LaTeX algorithm box (`Algorithm 1 Construction process of TIDE`) in Appendix A\[cite: 38\].

&#32; 

&#32; 

## SAMPLE 3: JaxMARL-BC: Multi-Agent Reinforcement Learning for Macroeconomic Modelling, in Seconds

### Excerpt

"Multi-agent reinforcement learning (MARL) offers a principled way of populating simulated economies with many heterogeneous decision makers. Its adoption, pioneered in finance, has nonetheless been slow in macroeconomics because of two main limitations: the lack of a shared frame of reference connecting MARL systems to dynamic stochastic general equilibrium (DSGE) models the profession already trusts, and the very long training times. The first limitation was recently addressed by the Multi-Agent Reinforcement Learning Business Cycle (MARL-BC), which places deep RL households in a real business cycle economy and reduces to classic DSGE models in specific limits."

### Report:

Extracted Sections

- **Title:** JaxMARL-BC: Multi-Agent Reinforcement Learning for Macroeconomic Modelling, in Seconds\[cite: 65\]
- **Author List:** Daniele Montagnani (Università di Pavia), Andrea Coletta (Banca d'Italia), Antonietta Mira (USI Lugano, Università dell'Insubria), Aldo Glielmo\* (Banca d'Italia)\[cite: 65\]
- **Abstract:** Multi-agent reinforcement learning (MARL) offers a principled way of populating simulated economies with many heterogeneous decision makers. Its adoption, pioneered in finance, has nonetheless been slow in macroeconomics because of two main limitations: the lack of a shared frame of reference connecting MARL systems to dynamic stochastic general equilibrium (DSGE) models the profession already trusts, and the very long training times. The first limitation was recently addressed by the Multi-Agent Reinforcement Learning Business Cycle (MARL-BC), which places deep RL households in a real business cycle economy and reduces to classic DSGE models in specific limits. Here we address the second limitation. We present JaxMARL-BC, a JAX-accelerated simulator that trains MARL-BC economies in seconds (between 75x and 724x faster than the reference implementation), and scales to 200,000 independent learning households. We verify its correctness against the known DSGE limits, characterise its scaling through a simple cost law, and demonstrate its value by a proof-of-concept calibration of an extended model with heterogeneous returns on capital, in a two-hour experiment that would previously have taken over a month. We release JaxMARL-BC as open source.\[cite: 65\]
- **Reference Section:**
  > **References**\[cite: 72\]
  >
  > \[1\] Stéphane Adjemian, Houtan Bastani, Michel Juillard, Frédéric Karamé, Junior Maih, Ferhat Mihoubi, Willi Mutschler, George Perendia, Johannes Pfeifer, Marco Ratto, and Sébastien Villemot. 2011. Dynare: Reference Manual, Version 4. Dynare Working Paper 1. CEPREMAP.\[cite: 72\]
  >
  > \[2\] Akash Agrawal, Joel Dyer, Aldo Glielmo, and Michael J. Wooldridge. 2025. Robust Policy Design in Agent-Based Simulators using Adversarial Reinforcement Learning. In _The First MARW: Multi-Agent AI in the Real World Workshop at AAAI 2025_.\[cite: 72\]
  >
  > \[3\] Stefano V. Albrecht, Filippos Christianos, and Lukas Schäfer. 2024. _Multi-Agent Reinforcement Learning: Foundations and Modern Approaches_. MIT Press.\[cite: 72\]
  >
  > _(... 50 entries total, spanning pages 7–8)_\[cite: 72, 73\]

Layout, Formatting, and Formatting Patterns

- **DOI Appearance & Position:**
  - **Page & Location:** Top left header of Page 1 shows the arXiv identifier\[cite: 65\]. DOIs are embedded within reference citations on Page 7–8\[cite: 72, 73\].

  - **Format:** Header contains `arXiv:2610.28907v1 [cs.MA] 20 Oct 2026`\[cite: 65\]. Reference section includes HTTPS DOI links like `[`[`https://doi.org/10.1145/3768292.3770348`](https://doi.org/10.1145/3768292.3770348)`](`[`https://doi.org/10.1145/3768292.3770348`](https://doi.org/10.1145/3768292.3770348)`)`\[cite: 72\].

  - **Excerpt:**

    Plaintext

    ```
    arXiv:2610.28907v1 [cs.MA] 20 Oct 2026
    
    ```

    Plaintext

    ```
    https://doi.org/10.1145/3768292.3770348
    
    ```
- **Reference Section Start:**
  - Begins on Page 7 immediately following Section 6 (Conclusions), titled `References`\[cite: 71, 72\].

  - **Excerpt:**

    Plaintext

    ```
    References
    [1] Stéphane Adjemian, Houtan Bastani...
    
    ```
- **Reference Numbering & Formatting:**
  - **Formatting Style:** Uses numeric bracketed labels `[1]`, `[2]`, `[3]` in alphabetical order\[cite: 72\]. In-text references use numeric citations (e.g., `[44]`, `[3]`, `[12, 14, 50]`)\[cite: 65\].

  - **Excerpt:**

    Plaintext

    ```
    [1] Stéphane Adjemian, Houtan Bastani, Michel Juillard... 2011. Dynare: Reference Manual...
    
    ```
- **Layout Quirks:**
  - **Two-Column Conference Format:** Styled according to ACM conference standards (ICAIF template), featuring a two-column body layout\[cite: 65\].
  - **Conference Notice Banner:** Left column on Page 1 contains a dedicated footnote box denoting publication details (`Accepted at the 7th ACM International Conference on AI in Finance (ICAIF 26)`)\[cite: 65\].
  - **Dense Inline Figures:** Contains multi-panel plots spanning across both columns (e.g., Figure 1, Figure 3, Figure 6)\[cite: 67, 69, 72\].

&#32; 

## PROMPT

"I'm attaching 3 open-access research papers (mix of two-column conference, single-column, many-author). For each: extract the title, author list, abstract, and the reference section. Then describe the exact patterns you observe: where the DOI appears (page, position, format), how the reference section starts, how references are numbered/formatted, and any layout quirks. Give short real excerpts to illustrate each pattern. Output as a per-paper report."