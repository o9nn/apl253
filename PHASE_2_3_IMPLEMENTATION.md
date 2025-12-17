# Pattern Language Implementation Guide

## Phase 2 & 3 Implementation: Query, Transformation & Cognitive Enhancement

This guide documents the implementation of Phase 2 and Phase 3 components from PARADIGM_LANGUAGE_ANALYSIS.md.

## Overview

The implementation provides cognitive affordances for achieving "optimal grip" on the pattern language gestalt salience landscape through:

1. **Datalog Query System** - Declarative pattern queries and relationship inference
2. **Salience Scoring System** - Context-based pattern relevance and importance
3. **Unified API** - Integrated interface for pattern exploration and discovery

## Components

### 1. Datalog Query System (`pattern_query_datalog.py`)

Implements declarative queries over the pattern language using pyDatalog.

**Key Features:**
- Load patterns from JSON schema
- Load facts from OpenCog Atomese .scm files
- Inference rules for transitive dependencies
- Category and sequence queries
- Pattern relationship discovery

**Usage Example:**
```python
from pattern_query_datalog import PatternQuerySystem

# Initialize system
system = PatternQuerySystem()
system.load_from_json("pattern_language_generated.json")

# Query patterns in a category
towns = system.query_patterns_in_category('Towns')

# Find related patterns
related = system.query_related_patterns('apl12')

# Check for dependency paths
has_path = system.find_pattern_path('apl1', 'apl2')

# Get full context
context = system.get_pattern_context('apl12')
```

**Cognitive Affordances:**
- Multi-scale perception (categories → sequences → patterns)
- Declarative queries ("what" not "how")
- Transitive inference (dependency chains)
- Fluid navigation (related patterns, paths)

**Tests:** `test_pattern_query_datalog.py` (20 tests, all passing)

---

### 2. Salience Scoring System (`pattern_salience_scorer.py`)

Implements multi-factor salience scoring for patterns.

**Key Features:**
- Network centrality analysis (PageRank, betweenness)
- Context-based relevance scoring
- Gestalt emergence detection
- Force resonance scoring
- Pattern clustering (community detection)

**Salience Factors:**
1. **Centrality** (20% weight) - Structural importance in pattern network
2. **Relevance** (30% weight) - Match to context keywords
3. **Gestalt** (30% weight) - Fit with active patterns
4. **Force** (20% weight) - Resonance with problem forces

**Usage Example:**
```python
from pattern_salience_scorer import PatternSalienceScorer

# Initialize scorer
scorer = PatternSalienceScorer()
scorer.load_from_json("pattern_language_generated.json")

# Compute centrality
centrality = scorer.compute_centrality()

# Rank patterns by salience
top = scorer.rank_patterns(
    context_keywords=['community', 'housing'],
    active_patterns={'apl12', 'apl13'},
    problem_forces=['social cohesion'],
    top_k=10
)

# Find pattern clusters (gestalts)
clusters = scorer.find_pattern_clusters(min_size=5)

# Compute specific pattern salience
score = scorer.compute_salience(
    'apl12',
    context_keywords=['neighborhood'],
    active_patterns={'apl13'}
)
```

**Cognitive Affordances:**
- Context guides attention to relevant patterns
- Centrality identifies important patterns
- Gestalt scores reveal emergent relationships
- Clustering discovers natural pattern groupings

**Tests:** `test_pattern_salience_scorer.py` (25 tests, all passing)

---

### 3. Unified API (`pattern_language_api.py`)

Integrates query and salience systems into a unified interface.

**Key Features:**
- Pattern retrieval and search
- Category and sequence navigation
- Relationship queries
- Context-based ranking
- Pattern exploration
- Statistics and summaries

**Usage Example:**
```python
from pattern_language_api import PatternLanguageAPI

# Initialize API
api = PatternLanguageAPI()

# Get statistics
stats = api.get_statistics()

# Search patterns
results = api.search_patterns('community', max_results=10)

# Get pattern context
context = api.get_pattern_context('apl12')

# Explore from a pattern
exploration = api.explore_from_pattern(
    'apl12',
    context_keywords=['neighborhood', 'housing']
)

# Rank by salience
top = api.rank_by_salience(
    context_keywords=['community', 'pedestrian'],
    top_k=10
)

# Get central patterns
central = api.get_central_patterns(top_k=10)
```

**API Methods:**

**Pattern Retrieval:**
- `get_pattern(pattern_id)` - Get pattern by ID
- `get_all_patterns()` - Get all patterns
- `search_patterns(query, max_results)` - Text search

**Categories & Sequences:**
- `get_categories()` - All categories
- `get_patterns_in_category(category)` - Patterns in category
- `get_sequences()` - All sequences
- `get_patterns_in_sequence(sequence_id)` - Patterns in sequence
- `get_sequences_containing(pattern_id)` - Sequences containing pattern

**Relationships:**
- `get_related_patterns(pattern_id)` - Related by category/sequence
- `get_dependencies(pattern_id)` - Transitive dependencies
- `has_path(from_pattern, to_pattern)` - Check dependency path

**Salience & Context:**
- `rank_by_salience(context, active, forces, top_k)` - Rank patterns
- `compute_pattern_salience(pattern_id, context)` - Compute salience
- `get_pattern_context(pattern_id)` - Full pattern context
- `explore_from_pattern(pattern_id, context)` - Explore pattern space

**Discovery:**
- `find_pattern_clusters(min_size)` - Find pattern clusters
- `get_central_patterns(top_k)` - Most central patterns
- `get_statistics()` - Overall statistics

---

## Installation

### Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**
- `pyDatalog>=0.17.1` - Datalog query engine
- `networkx>=3.0` - Graph analysis
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations

See `requirements.txt` for full list.

---

## Running Demos

```bash
# Datalog query system demo
python3 pattern_query_datalog.py

# Salience scoring demo
python3 pattern_salience_scorer.py

# Unified API demo
python3 pattern_language_api.py
```

---

## Running Tests

```bash
# All tests
python3 -m pytest test_pattern_query_datalog.py test_pattern_salience_scorer.py -v

# Query system tests only
python3 -m pytest test_pattern_query_datalog.py -v

# Salience scorer tests only
python3 -m pytest test_pattern_salience_scorer.py -v
```

**Test Coverage:**
- Query system: 20 tests
- Salience scorer: 25 tests
- Total: 45 tests, all passing

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Pattern Language Unified API               │
│         (pattern_language_api.py)                       │
│  - Search & retrieval                                   │
│  - Navigation & exploration                             │
│  - Statistics & summaries                               │
└─────────────────┬───────────────────────┬───────────────┘
                  │                       │
        ┌─────────▼─────────┐   ┌────────▼──────────┐
        │  Query System     │   │  Salience Scorer  │
        │  (Datalog)        │   │  (Multi-factor)   │
        │                   │   │                   │
        │ - Categories      │   │ - Centrality      │
        │ - Sequences       │   │ - Relevance       │
        │ - Dependencies    │   │ - Gestalt         │
        │ - Relationships   │   │ - Force resonance │
        │ - Inference       │   │ - Clustering      │
        └───────────────────┘   └───────────────────┘
                  │                       │
                  └───────────┬───────────┘
                              │
                    ┌─────────▼──────────┐
                    │  Pattern Data      │
                    │  (JSON + Atomese)  │
                    │                    │
                    │ - 253 patterns     │
                    │ - 3 categories     │
                    │ - 36 sequences     │
                    │ - Relationships    │
                    └────────────────────┘
```

---

## Cognitive Affordances

The implementation provides specific cognitive affordances for optimal grip:

### 1. Multi-Scale Perception
Navigate from broad categories to specific patterns:
```python
# Categories → Patterns in category → Pattern details
categories = api.get_categories()
towns = api.get_patterns_in_category('Towns')
context = api.get_pattern_context('apl12')
```

### 2. Relationship Richness
Multiple types of relationships:
- Category membership (patterns in same domain)
- Sequence connection (patterns in same sequence)
- Dependencies (patterns that depend on others)
- Salience relationships (patterns relevant in same context)

### 3. Context-Sensitive Attention
Patterns become salient based on context:
```python
# Patterns relevant to community housing
top = api.rank_by_salience(
    context_keywords=['community', 'housing', 'neighborhood']
)
```

### 4. Gestalt Emergence
Patterns that naturally fit together:
```python
# Given active patterns, find complementary patterns
score = scorer.compute_gestalt_score('apl15', {'apl12', 'apl13'})
```

### 5. Structural Importance
Identify central patterns in the network:
```python
central = api.get_central_patterns(top_k=10)
```

---

## Data Format

### Pattern Language JSON Structure

```json
{
  "meta_pattern": { ... },
  "categories": [
    {
      "name": "Towns",
      "pattern_range": {"start": 1, "end": 94},
      "sequences": [
        {
          "id": 1,
          "patterns": [1, 2, 3, ...],
          ...
        }
      ]
    }
  ],
  "patterns": [
    {
      "id": "apl1",
      "number": 1,
      "name": "INDEPENDENT REGIONS",
      "problem": "...",
      "solution": "...",
      "preceding_patterns": [],
      "following_patterns": [2, 8]
    }
  ]
}
```

---

## Next Steps

### Remaining Phase 2 Items:
- [ ] Haskell domain transformation library
- [ ] FFI bindings for Python integration

### Remaining Phase 3 Items:
- [ ] Constraint-based pattern selection (OR-Tools)
- [ ] Advanced force resolution

### Phase 4: Visualization & Interaction
- [ ] D3.js interactive visualization
- [ ] Gestalt salience landscape viewer
- [ ] Pattern sequence animator

---

## References

- **PARADIGM_LANGUAGE_ANALYSIS.md** - Original analysis and architecture
- **QUICK_REFERENCE.md** - Quick reference for repository
- **CLAUDE.md** - Development context

---

## License

See LICENSE file in repository root.
