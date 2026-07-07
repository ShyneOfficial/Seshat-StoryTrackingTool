# Seshat

> **⚠️ Work in Progress**
>
> This repository contains the early Proof of Concept (PoC) of **Seshat**, a modular story-state engine for writers.
>
> The project is currently in active development and serves as a research playground to validate its architecture and core concepts before becoming a complete application.

---

# Overview

## Status

🚧 **Research Prototype (PoC)**

Current version: **v0.0.1**

Seshat is an experimental writing assistant designed to help authors maintain the continuity of their stories.

Rather than acting as another worldbuilding wiki or manuscript editor, Seshat aims to understand how a story evolves over time.

By analyzing chapters, it builds a structured representation of the story's current state, allowing authors to easily answer questions such as:

* Which characters have already been introduced?
* What does the reader know at Chapter 18?
* Which locations have been explored?
* What skills has the protagonist learned so far?
* Which plot elements have already appeared?

The long-term vision is to provide an intelligent continuity layer that sits alongside existing writing tools.

---

# Current Goal

This repository focuses on the first Proof of Concept:

> Building a modular NLP pipeline capable of extracting structured story information from raw chapter text.

The objective is **not** to create a perfect AI, but to validate the architecture that will power Seshat.

---

# Roadmap (Current Proof of Concept)

## Week 1 — NLP Pipeline

Develop a modular NLP pipeline capable of analyzing chapters and extracting structured story events.

The first implementation focuses on two modules.

### Character Module

* Detect known characters
* Detect newly introduced characters
* Track character appearances
* Track the current known location of each character
* Track visited locations

### Location Module

* Detect known locations
* Detect newly discovered locations
* Track explored and visited places

The pipeline should output structured events instead of raw text analysis.

---

## Week 2 — Prototype Website

Develop a minimal web application demonstrating the NLP pipeline.

The prototype will include:

* Story management
* Chapter import / paste
* NLP analysis
* Validation and modification of detected events
* Character browser
* Location browser
* Search functionality
* Hoverable entities displaying contextual information
* Chapter-based story state visualization

The focus is on demonstrating the architecture rather than building a production-ready application.

---

# Architecture Vision

Seshat is built around a modular architecture.

Each module is responsible for a specific aspect of the story.

Examples include:

* Characters
* Locations
* Items
* Skills
* Quests
* Lore
* Factions
* Relationships

Each module will eventually define:

* Its own data model
* The events it understands
* NLP extraction rules
* Validation logic
* Story-state update rules
* User interface components

This architecture allows Seshat to adapt to different genres and writing styles by enabling only the modules relevant to a given story.

---

# Future Vision

After the NLP proof of concept, future iterations will introduce:

* AI-assisted (LLM) extraction for ambiguous cases
* Plugin-based module system
* Story timeline reconstruction
* Reader knowledge visualization
* Continuity checking
* Narrative consistency reports
* Story-state snapshots
* Searchable event history

The long-term goal is to build a **story-state engine** capable of understanding how a narrative evolves chapter by chapter.

---

# Project Status

Current development status:

* [ ] Modular NLP pipeline
* [ ] Character Module
* [ ] Location Module
* [ ] Event extraction engine
* [ ] Prototype web interface
* [ ] Story-state engine
* [ ] LLM-assisted extraction
* [ ] Plugin system

---

# Technologies (Planned)

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Tiptap

### Backend

* Next.js API
* Python
* FastAPI

### NLP

* spaCy
* Rule-based extraction
* Custom module extractors

### Database

* PostgreSQL
* Prisma ORM

---

# Repository Purpose

This repository is primarily intended to experiment with:

* Modular software architecture
* Natural Language Processing
* Story-state reconstruction
* Narrative event extraction
* Chapter-by-chapter continuity tracking

Feedback, ideas and contributions are always welcome as Seshat continues to evolve.
