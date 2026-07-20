# Seshat — NLP Pipeline

> **Work in Progress**
>
> This branch contains the first prototype of Seshat’s modular NLP pipeline.

---

# Overview

Seshat is a story-state engine designed to help writers track story continuity across chapters.

This branch focuses on the **analysis pipeline**: taking raw chapter text and turning it into structured data.

Current pipeline output includes:

* Character mentions
* Location mentions
* Simple character-location visit links
* Warnings and errors from analysis modules

---

# Current Architecture

```txt
Raw chapter text
↓
spaCy Doc
↓
Seshat modules
↓
AnalysisResult
```

The pipeline is split into clear parts:

```txt
app/
├── schemas/      # Dataclasses for analysis results
├── pipeline/     # Pipeline execution and context
├── modules/      # Entity and link extraction modules
├── utils/        # Shared helpers
└── main.py       # Test entry point
```

---

# Current Modules

## CharacterModule

Detects characters using spaCy `PERSON` entities.

## LocationModule

Detects locations using:

* spaCy location labels: `GPE`, `LOC`, `FAC`
* simple keyword rules such as `forest`, `city`, `castle`, `river`

## VisitModule

Creates a `visit` link when a character and a location appear in the same sentence.

This is temporary and will be improved later with better grammar and movement detection.

---

# Analysis Result

The pipeline returns an `AnalysisResult` containing:

```txt
chapter_id
entities
links
warnings
errors
```

Entity mentions represent detected characters or locations.

Links represent relationships between entities, such as:

```txt
Owen visited the forest
```

---

# Installation

```bash
make setup
```

This creates the virtual environment, installs dependencies, and downloads the spaCy model.

---

# Run

Create an input file:

```txt
data/input1.txt
```

Then run:

```bash
make run
```

The current test entry point is:

```txt
app/main.py
```

---

# Current Limitations

This is an early prototype.

Known limitations:

* Character detection depends on spaCy.
* Location detection is partly keyword-based.
* Visit detection only checks same-sentence matches.
* No alias resolution yet.
* No database persistence yet.
* No validation UI yet.

---

# Next Step

The next step is to add a data-management layer.

Planned flow:

```txt
AnalysisResult
↓
DataManager
↓
Database
```

The database manager will organize analysis results into persistent story data, including:

* Chapters
* Unique entities
* Entity mentions
* Links
* Link participants

The analysis pipeline should stay separate from database logic.
