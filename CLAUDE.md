# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

dead-software is a learning material repository for software engineering — architecture patterns and design patterns with minimal runnable Python code examples. Target audience: mixed (beginners to experienced developers entering the field in the AI coding era).

## Running Examples

Every topic has `example.py` (and optional `advanced.py`). Run with:

```bash
python architectures/layered/example.py
python design-patterns/observer/example.py
```

No pip install needed — all examples use only the Python standard library.

## Adding New Topics

Each topic directory follows this structure:
- `README.md` — standard template (What is / Core Idea / Code Example / Pros and Cons / Real-World Applications / Further Reading)
- `example.py` — minimal runnable example (< 80 lines, output-driven)
- `advanced.py` — optional progressive example

Place architecture topics under `architectures/`, design pattern topics under `design-patterns/`.

## Code Principles

- Python standard library only
- Single-file runnable (`python example.py` produces clear output)
- Under 80 lines, demonstrating only core mechanism
- Comments explain why, not just what — connecting code to concept
- Output-driven: printed output demonstrates what the pattern/architecture does

## Directory Structure

```
architectures/          # Macro architecture patterns
  layered/
  event-driven/
  microservices/
  pipeline/
design-patterns/        # Micro design patterns
  observer/
  strategy/
  factory/
  decorator/
solid/                  # SOLID principles
  srp/
  ocp/
  lsp/
  isp/
  dip/
concurrency/            # Concurrency patterns
  producer-consumer/
  reactor/
  read-write-lock/
  future-promise/
anti-patterns/          # Anti-patterns
  god-object/
  tight-coupling/
  premature-optimization/
  copy-paste-programming/
shared/                 # Shared utilities
```
