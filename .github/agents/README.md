# Nested Agency Structure

This directory contains a complete nested agency structure for the Pattern Language (APL 253), organized as a hierarchical knowledge base with multiple dimensional perspectives.

## Overview

The structure implements a comprehensive organization of 253 patterns across 6 dimensions, 3 categories, and 36 sequences, creating a multi-dimensional navigation system for pattern exploration.

## Directory Structure

```
/apl253/.github/agents/
├── apl0.md                          # Meta-pattern 0 definition - main language
├── apl0/                            # Meta-pattern 0 folder
│   ├── archetypal.md                # Archetypal dimension (A)
│   ├── archetypal/                  # Archetypal folder
│   │   ├── towns.md                 # Towns category
│   │   ├── towns/                   # Towns folder
│   │   │   ├── seq01.md             # Sequence 01
│   │   │   ├── seq01/               # Sequence 01 folder
│   │   │   │   ├── apl001.md        # Pattern 001
│   │   │   │   ├── apl001/          # Pattern 001 references
│   │   │   │   │   ├── broader.md   # Broader patterns
│   │   │   │   │   ├── narrower.md  # Narrower patterns
│   │   │   ├── seq02.md             # Sequence 02
│   │   │   ├── seq02/               # Sequence 02 folder
│   │   │   └── ...                  # (sequences 01-15)
│   │   ├── buildings.md             # Buildings category
│   │   ├── buildings/               # Buildings folder
│   │   │   ├── seq16.md             # Sequence 16
│   │   │   └── ...                  # (sequences 16-28)
│   │   ├── construction.md          # Construction category
│   │   ├── construction/            # Construction folder
│   │   │   ├── seq29.md             # Sequence 29
│   │   │   └── ...                  # (sequences 29-36)
│   ├── template.md                  # Template dimension (T)
│   ├── template/                    # Template folder (same structure)
│   ├── physical.md                  # Physical dimension (P)
│   ├── physical/                    # Physical folder (same structure)
│   ├── social.md                    # Social dimension (S)
│   ├── social/                      # Social folder (same structure)
│   ├── conceptual.md                # Conceptual dimension (C)
│   ├── conceptual/                  # Conceptual folder (same structure)
│   ├── interpersonal.md             # Interpersonal dimension (I)
│   ├── interpersonal/               # Interpersonal folder (same structure)
```

## Structural Components

### Meta-Pattern (Level 0)
- **apl0.md**: Defines the entire Pattern Language system
- Contains overview of all 6 dimensions, 3 categories, 36 sequences, and 253 patterns

### Dimensions (Level 1)
Six dimensional perspectives, each containing the full pattern hierarchy:

1. **Archetypal (A)**: Abstract patterns with domain-specific placeholders ({{domains}}, {{frameworks}}, etc.)
2. **Template (T)**: Generic template patterns serving as basis for variations
3. **Physical (P)**: Spatial, material, architectural manifestations
4. **Social (S)**: Organizational, community, institutional expressions
5. **Conceptual (C)**: Knowledge, theoretical, paradigmatic realizations
6. **Interpersonal (I)**: Awareness, consciousness, mental structures

### Categories (Level 2)
Three scale-based categories within each dimension:

1. **Towns** (Patterns 1-94): Large-scale patterns - regions, cities, communities, neighborhoods
2. **Buildings** (Patterns 95-204): Medium-scale patterns - structures, spaces, layouts
3. **Construction** (Patterns 205-253): Small-scale patterns - details, materials, techniques

### Sequences (Level 3)
36 thematic sequences organizing related patterns:

- **Towns**: Sequences 01-15 (15 sequences)
  - Seq 01: Regions instead of countries
  - Seq 02: Regional policies
  - Seq 03: Major structures which define the city
  - ... (through seq 15)

- **Buildings**: Sequences 16-28 (13 sequences)
  - Seq 16: Building layout
  - Seq 17: Building character
  - ... (through seq 28)

- **Construction**: Sequences 29-36 (8 sequences)
  - Seq 29: Construction process
  - Seq 30: Materials
  - ... (through seq 36)

### Patterns (Level 4)
253 individual patterns distributed across sequences:

- Each pattern file includes:
  - Pattern ID, number, and dimension
  - Full pattern content (problem, solution, discussion)
  - Asterisk importance rating (0-2)
  
- Each pattern has a relations folder containing:
  - **broader.md**: Preceding patterns (context)
  - **narrower.md**: Following patterns (details)

## Statistics

- **1** Meta-pattern definition (apl0.md)
- **6** Dimensions (A, T, P, S, C, I)
- **18** Category files (3 per dimension)
- **216** Sequence files (36 per dimension)
- **1,560** Pattern files (260 per dimension, some patterns appear in multiple sequences)
- **1,560** Pattern relation folders

## Navigation Examples

### View Pattern 1 in Archetypal Dimension:
```
.github/agents/apl0/archetypal/towns/seq01/apl001.md
```

### View Pattern 132 in Physical Dimension:
```
.github/agents/apl0/physical/buildings/seq20/apl132.md
```

### View Pattern 253 in Social Dimension:
```
.github/agents/apl0/social/construction/seq36/apl253.md
```

### View Relations for Pattern 1:
```
.github/agents/apl0/archetypal/towns/seq01/apl001/broader.md
.github/agents/apl0/archetypal/towns/seq01/apl001/narrower.md
```

## Usage

This structure enables multiple ways to navigate the Pattern Language:

1. **By Dimension**: Choose a perspective (Archetypal, Physical, Social, etc.) to view all patterns through that lens
2. **By Scale**: Navigate from large (Towns) to medium (Buildings) to small (Construction)
3. **By Sequence**: Follow thematic flows of related patterns
4. **By Relations**: Trace pattern connections through broader/narrower relationships

## Generation

The structure is generated by `generate_nested_agency.py` from source data:
- `pattern_language_generated.json` (meta-pattern and full pattern data)
- `pattern_sequences.json` (36 sequences with pattern mappings)
- `category_*.json` (Towns, Buildings, Construction definitions)
- `markdown/apl/*.md` (individual pattern content)

## Verification

Run `verify_nested_agency.py` to validate the complete structure:
```bash
python3 verify_nested_agency.py
```

This verifies:
- All meta-pattern, dimension, category, and sequence files exist
- All pattern files and relation folders are created
- Counts match expected totals

## Philosophy

This nested structure reflects Christopher Alexander's vision of a "pattern language" as:
- **Hierarchical**: Patterns at different scales
- **Interconnected**: Each pattern links to related patterns
- **Generative**: Patterns combine to create emergent phenomena
- **Multi-dimensional**: Same patterns viewed through different lenses

The structure enables exploration of how architectural patterns can be understood as:
- Abstract templates (Archetypal)
- Physical spaces (Physical)
- Social organizations (Social)
- Conceptual frameworks (Conceptual)
- Psychological structures (Interpersonal)
