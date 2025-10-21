# p235

This repository contains collections of design patterns and organizational metaphors:

## Original Collections

- **APL**: Christopher Alexander's "A Pattern Language" (253 patterns) - architectural and urban design patterns
- **UIA**: Union of International Associations "Patterns & Metaphors" (253 patterns) - organizational and conceptual patterns

## Markdown Versions

The `markdown/` directory contains converted versions of all APL and UIA pages in markdown format for improved readability and accessibility:

- **`markdown/apl/`**: 253 A Pattern Language patterns (apl001.md - apl253.md)
- **`markdown/uia/`**: 253 UIA Patterns & Metaphors (12610010.md - 12612530.md)

See `markdown/README.md` for detailed information about the conversion process and markdown structure.

## Pattern Language Schema

The repository includes a formalized JSON schema for the Pattern Language:

- **Pattern Language Schema** (`pattern_language_generated.json`) - Complete meta-pattern, categories, and sequences
- **Pattern Sequences** (`pattern_sequences.json`) - All 36 pattern sequences with emergent phenomena
- **Categories** (`category_*.json`) - Towns, Buildings, and Construction categories

See `PATTERN_SCHEMA_README.md` for detailed information about the schema structure.

## OpenCog Atomese Representation

The Pattern Language has been converted to OpenCog's Atomese format for knowledge representation and pattern matching:

- **`opencog_atomese/`** - Complete Atomese hypergraph representation in Scheme format
  - `pattern_language.scm` - Complete representation
  - `meta_pattern.scm` - Meta-pattern
  - `categories.scm` - Categories with InheritanceLinks
  - `sequences.scm` - Sequences with MemberLinks
  - **Enhanced Features:**
    - `pattern_language_enhanced.scm` - Enhanced with diagrams, details, and connections
    - `relationship_types.scm` - Pattern relationship types (complement, conflict, alternative)
    - `patterns/` - Individual .scm files for modular loading

The Atomese format enables:
- Pattern matching and reasoning in OpenCog
- Hypergraph queries for pattern relationships
- Knowledge graph navigation and inference
- Integration with AI/AGI systems

See `opencog_atomese/README.md` for usage examples and `opencog_atomese/ENHANCEMENTS.md` for enhanced features documentation.

### Generating Atomese Files

```bash
# Generate base Atomese files
python3 generate_opencog_atomese.py

# Generate enhanced features
python3 generate_enhanced_atomese.py
```

### Testing Atomese Files

```bash
# Test base files
python3 test_opencog_atomese.py

# Test enhanced features
python3 test_enhanced_atomese.py
```

### Demo Enhanced Features

```bash
python3 demo_enhanced_atomese.py
```