# Dead-Software: Software Engineering Learning Material Design

## Project Positioning

**dead-software** is a learning material repository for software engineering aimed at a mixed audience (from beginners to experienced developers). It helps engineers entering the field in the AI coding era understand the overall landscape of software engineering. Each topic includes concise explanatory documentation and minimal runnable Python code examples.

The name "dead-software" reflects the reality that AI coding is dramatically changing software engineering — newcomers may miss traditional growth experiences, yet still need a holistic understanding of software engineering principles.

## Target Audience

Mixed audience with progressive content:
- **Beginners**: Start from basic concepts (what is layered architecture), with the simplest possible code
- **Experienced coders**: Focus on architectural thinking and design trade-offs, with moderately complex examples
- Each topic provides a progression from simple (`example.py`) to more detailed (`advanced.py`, optional)

## Code Language & Style

- **Primary language**: Python
- **Dependencies**: Python standard library only (no external packages), unless the topic inherently requires it (e.g., microservices uses `http.server`)
- **Runnable**: `python example.py` produces clear output
- **Compact**: `example.py` < 80 lines, demonstrating only the core mechanism
- **Output-driven**: Code prints clear output so readers see what the architecture/pattern actually does

## Project Structure

```
dead-software/
├── README.md                # Project intro + navigation index
├── architectures/           # Macro architecture patterns
│   ├── layered/             # Layered architecture
│   │   ├── README.md
│   │   ├── example.py
│   │   └── advanced.py      # Optional
│   ├── event-driven/        # Event-driven architecture
│   ├── microservices/       # Microservices architecture
│   └── pipeline/            # Pipeline/filter architecture
├── design-patterns/         # Micro design patterns
│   ├── observer/            # Observer pattern
│   ├── strategy/            # Strategy pattern
│   ├── factory/             # Factory pattern
│   ├── decorator/           # Decorator pattern
└── shared/                  # Shared test utilities/helpers
```

Two top-level categories provide clear separation:
- `architectures/` — macro patterns that shape system structure
- `design-patterns/` — micro patterns that solve specific design problems
- Readers can choose their own learning path based on needs

## Topic README.md Template

Every topic directory follows this standard template:

```markdown
# [Topic Name]

## What is [Topic]
<!-- One-paragraph definition for quick understanding -->

## Core Idea
<!-- A few sentences capturing the essential principle, with simple diagram if needed -->

## Code Example
<!-- Guide reader to run example.py, then walk through key code segments -->

## Advanced Example (if present)
<!-- Guide reader to run advanced.py, showing a more realistic scenario -->

## Pros and Cons
<!-- Objective listing of applicable scenarios and limitations -->

## Real-World Applications
<!-- 1-2 well-known projects/frameworks using this pattern -->

## Further Reading
<!-- Recommended authoritative books, articles, video links -->
```

## First Batch: 8 Topics

### Architecture Patterns (4)

| Topic | Directory | example.py Demonstration |
|-------|-----------|--------------------------|
| Layered Architecture | `architectures/layered/` | Three-layer separation (presentation/business/data) |
| Event-Driven Architecture | `architectures/event-driven/` | Event bus + publish-subscribe |
| Microservices Architecture | `architectures/microservices/` | Multiple independent services communicating via HTTP |
| Pipeline Architecture | `architectures/pipeline/` | Data flowing through multiple processing stages |

### Design Patterns (4)

| Topic | Directory | example.py Demonstration |
|-------|-----------|--------------------------|
| Observer Pattern | `design-patterns/observer/` | One-to-many dependency notification between objects |
| Strategy Pattern | `design-patterns/strategy/` | Interchangeable algorithm family encapsulation |
| Factory Pattern | `design-patterns/factory/` | Centralized object creation logic management |
| Decorator Pattern | `design-patterns/decorator/` | Dynamically adding responsibilities to objects |

## Code Example Principles

1. **Standard library only**: No pip install needed (exceptions documented in README)
2. **Single-file runnable**: `python example.py` shows output immediately
3. **Under 80 lines**: Only the core mechanism, no unnecessary details
4. **Progressive**: `example.py` is the minimal version; `advanced.py` (optional) shows a slightly more complex variant
5. **Output-driven**: Clear printed output demonstrates what the pattern/architecture actually does
6. **Well-commented**: Comments explain why, not just what — connecting code to the concept

## Extension Strategy

- Start with 8 high-quality core topics
- Add new topics incrementally (each follows the same template)
- Potential future categories: concurrency patterns, SOLID principles, anti-patterns
- Each new topic follows the established README.md template and code principles
