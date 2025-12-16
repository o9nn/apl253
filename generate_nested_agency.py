#!/usr/bin/env python3
"""
Generate nested agency structure for .github/agents/

Directory Structure:
/apl253/.github/agents/
├── apl0.md                        # Meta-pattern 0 definition
├── apl0/                          # Meta-pattern 0 folder
│   ├── dim0.md                    # Dimension 0 (Archetypal)
│   ├── dim0/                      # Dimension 0 folder
│   │   ├── cat1.md                # Category 1 (Towns in physical dimension)
│   │   ├── cat1/                  # Category 1 folder
│   │   │   ├── seq01.md           # Sequence 01
│   │   │   ├── seq01/             # Sequence 01 folder
│   │   │   │   ├── apl001.md      # Pattern 001
│   │   │   │   ├── apl001/        # Pattern 001 references
│   │   ├── cat2.md                # Category 2 (Buildings in physical dimension)
│   │   ├── cat2/                  # Category 2 folder
│   │   ├── cat3.md                # Category 3 (Construction in physical dimension)
│   │   ├── cat3/                  # Category 3 folder
│   ├── dim1.md                    # Dimension 1 (Template)
│   ├── dim1/                      # Dimension 1 folder
│   ├── dim2.md                    # Dimension 2 (Physical)
│   ├── dim2/                      # Dimension 2 folder
│   ├── dim3.md                    # Dimension 3 (Social)
│   ├── dim3/                      # Dimension 3 folder
│   ├── dim4.md                    # Dimension 4 (Conceptual)
│   ├── dim4/                      # Dimension 4 folder
│   ├── dim5.md                    # Dimension 5 (Interpersonal)
│   ├── dim5/                      # Dimension 5 folder
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def load_json(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_meta_pattern_md(base_path: Path) -> None:
    """Create the meta-pattern 0 definition (apl0.md)"""
    content = """# Meta-Pattern 0: A Pattern Language

## Overview
This is the meta-pattern that defines the entire Pattern Language system consisting of 253 interconnected patterns organized across multiple dimensions and scales.

## Structure
- **6 Dimensions**: dim0-dim5 (Archetypal, Template, Physical, Social, Conceptual, Interpersonal)
- **3 Categories**: cat1-cat3 (meaning varies by dimension)
- **36 Sequences**: Organized flows of related patterns
- **253 Patterns**: Individual design solutions

## Purpose
A Pattern Language is a philosophy of human use of space and analysis of what makes humans comfortable in the space they inhabit. It provides a structured way to understand and create environments that support human life.

## Key Concepts
1. **Hierarchical Organization**: From large-scale to small-scale patterns
2. **Network of Connections**: Each pattern links to related patterns
3. **Emergent Phenomena**: Sequences create synergies between patterns
4. **Cross-Dimensional**: Same patterns can be viewed through different dimensional lenses

## Dimensions

### dim0 - Archetypal (A)
Abstract patterns using placeholders like {{domains}}, {{frameworks}}, {{elements}} that can be instantiated in any domain.

### dim1 - Template (T)
Generic template patterns that serve as basis for domain-specific variations.

### dim2 - Physical (P)
Spatial, material, and architectural manifestations of patterns in the built environment.
- cat1: Towns (Patterns 1-94) - Large-scale patterns
- cat2: Buildings (Patterns 95-204) - Medium-scale patterns
- cat3: Construction (Patterns 205-253) - Small-scale patterns

### dim3 - Social (S)
Organizational, community, and institutional expressions of patterns in social systems.

### dim4 - Conceptual (C)
Knowledge, theoretical, and paradigmatic realizations of patterns in abstract domains.

### dim5 - Interpersonal (I)
Awareness, consciousness, and mental structures that embody patterns in human psychology.

## Categories

Categories are numbered cat1, cat2, cat3 and their meaning varies by dimension:
- **dim2 (Physical)**: cat1=Towns, cat2=Buildings, cat3=Construction
- **Other dimensions**: Categories take on dimension-appropriate meanings

## Usage
Navigate through the dimensional folders to explore patterns from different perspectives. Each dimension contains the same organizational structure (categories → sequences → patterns) but with dimension-specific content.
"""
    filepath = base_path / "apl0.md"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_dimension_md(base_path: Path, dim_num: int, dim_name: str, description: str) -> None:
    """Create dimension definition markdown"""
    content = f"""# dim{dim_num} - {dim_name} Dimension

## Description
{description}

## Structure
This dimension contains the same organizational hierarchy as all others:
- **3 Categories**: cat1, cat2, cat3
- **36 Sequences**: Pattern flows organized by theme
- **253 Patterns**: Individual patterns viewed through the {dim_name.lower()} lens

## Navigation
Explore the categories below to find sequences and patterns relevant to the {dim_name.lower()} perspective.

### Categories
- **cat1/** - Category 1 patterns
- **cat2/** - Category 2 patterns
- **cat3/** - Category 3 patterns
"""
    filepath = base_path / f"dim{dim_num}.md"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_category_md(base_path: Path, cat_num: int, info: Dict) -> None:
    """Create category definition markdown"""
    content = f"""# cat{cat_num} Category

## Description
{info['description']}

## Pattern Range
Patterns {info['pattern_range']['start']} to {info['pattern_range']['end']}

## Sequences
This category contains sequences that organize related patterns into coherent flows.

Navigate to the sequence folders below to explore specific pattern groups.
"""
    filepath = base_path / f"cat{cat_num}.md"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def create_sequence_md(base_path: Path, sequence: Dict) -> None:
    """Create sequence definition markdown"""
    seq_id = f"seq{sequence['id']:02d}"
    patterns_str = ", ".join([f"apl{p:03d}" for p in sequence['patterns']])
    
    content = f"""# Sequence {sequence['id']}: {sequence['heading']}

## Description
{sequence['description']}

## Category
{sequence['category']}

## Patterns
{patterns_str}

## Emergent Phenomena
{sequence['emergent_phenomena']}

## Overview
This sequence contains {len(sequence['patterns'])} pattern(s) that work together to create the emergent phenomena described above.
"""
    filepath = base_path / f"{seq_id}.md"
    filepath.write_text(content)
    print(f"Created: {filepath}")

def load_pattern_content(pattern_num: int, dim_num: int) -> str:
    """Load pattern content from markdown files"""
    # Try to load from appropriate markdown directory
    if dim_num == 0:  # archetypal
        # Search for archetypal pattern in arc directory
        arc_dir = Path("/home/runner/work/apl253/apl253/markdown/arc")
        # Archetypal patterns use UIA IDs, need to map from APL number
        # For now, use APL as fallback
        pass
    
    # Default to APL patterns
    apl_file = Path(f"/home/runner/work/apl253/apl253/markdown/apl/apl{pattern_num:03d}.md")
    if apl_file.exists():
        return apl_file.read_text()
    
    return f"# Pattern {pattern_num}\n\nPattern content not yet loaded."

def create_pattern_md(base_path: Path, pattern_num: int, pattern_info: Dict, dim_num: int) -> None:
    """Create pattern markdown file"""
    pattern_id = f"apl{pattern_num:03d}"
    
    # Load actual pattern content
    content = load_pattern_content(pattern_num, dim_num)
    
    # Add dimension-specific header
    header = f"""---
pattern_id: {pattern_id}
pattern_number: {pattern_num}
dimension: dim{dim_num}
asterisks: {pattern_info.get('asterisks', 0)}
---

"""
    
    filepath = base_path / f"{pattern_id}.md"
    filepath.write_text(header + content)
    print(f"Created: {filepath}")

def create_pattern_relations_folder(base_path: Path, pattern_num: int, pattern_info: Dict) -> None:
    """Create pattern relations folder with reference files"""
    pattern_id = f"apl{pattern_num:03d}"
    pattern_folder = base_path / pattern_id
    pattern_folder.mkdir(parents=True, exist_ok=True)
    
    # Create broader patterns reference
    if pattern_info.get('preceding_patterns'):
        broader_content = f"""# Broader Patterns for {pattern_id}

These patterns provide context and are typically applied before this pattern:

"""
        for p in pattern_info['preceding_patterns']:
            broader_content += f"- apl{p:03d}\n"
        
        (pattern_folder / "broader.md").write_text(broader_content)
    
    # Create narrower patterns reference
    if pattern_info.get('following_patterns'):
        narrower_content = f"""# Narrower Patterns for {pattern_id}

These patterns provide detail and are typically applied after this pattern:

"""
        for p in pattern_info['following_patterns']:
            narrower_content += f"- apl{p:03d}\n"
        
        (pattern_folder / "narrower.md").write_text(narrower_content)
    
    print(f"Created relations folder: {pattern_folder}")

def generate_nested_structure():
    """Generate the complete nested agency structure"""
    
    # Base path
    base_path = Path("/home/runner/work/apl253/apl253/.github/agents")
    
    # Load data
    pattern_lang = load_json("/home/runner/work/apl253/apl253/pattern_language_generated.json")
    sequences_data = load_json("/home/runner/work/apl253/apl253/pattern_sequences.json")
    
    # Category info (keyed by old names for data loading, but we'll use cat1, cat2, cat3)
    categories_data = {
        "cat1": load_json("/home/runner/work/apl253/apl253/category_towns.json"),
        "cat2": load_json("/home/runner/work/apl253/apl253/category_buildings.json"),
        "cat3": load_json("/home/runner/work/apl253/apl253/category_construction.json")
    }
    
    # Map old category names to new cat# names for sequence matching
    category_name_map = {
        "Towns": "cat1",
        "Buildings": "cat2",
        "Construction": "cat3"
    }
    
    # Create meta-pattern (apl0.md)
    create_meta_pattern_md(base_path)
    
    # Create apl0 folder
    apl0_path = base_path / "apl0"
    apl0_path.mkdir(parents=True, exist_ok=True)
    
    # Dimensions - now mapped to dim0-dim5
    dimensions = [
        ("Archetypal", "Abstract patterns with domain-specific placeholders that can be instantiated across any domain"),
        ("Template", "Generic template patterns serving as basis for domain-specific variations"),
        ("Physical", "Spatial, material, and architectural patterns in the built environment"),
        ("Social", "Organizational, community, and institutional patterns in social systems"),
        ("Conceptual", "Knowledge, theoretical, and paradigmatic patterns in abstract domains"),
        ("Interpersonal", "Awareness, consciousness, and mental patterns in human psychology")
    ]
    
    # Create each dimension (dim0 through dim5)
    for dim_num, (dim_name, description) in enumerate(dimensions):
        # Create dimension md
        create_dimension_md(apl0_path, dim_num, dim_name, description)
        
        # Create dimension folder
        dim_path = apl0_path / f"dim{dim_num}"
        dim_path.mkdir(parents=True, exist_ok=True)
        
        # Create categories within dimension (cat1, cat2, cat3)
        for cat_num, (cat_key, category_info) in enumerate(categories_data.items(), start=1):
            # Create category md
            create_category_md(dim_path, cat_num, category_info)
            
            # Create category folder
            cat_path = dim_path / f"cat{cat_num}"
            cat_path.mkdir(parents=True, exist_ok=True)
            
            # Get sequences for this category (using original category names from JSON)
            original_cat_name = category_info['name']  # "Towns", "Buildings", or "Construction"
            category_sequences = [s for s in sequences_data['sequences'] 
                                if s['category'] == original_cat_name]
            
            # Create sequences within category
            for sequence in category_sequences:
                # Create sequence md
                create_sequence_md(cat_path, sequence)
                
                # Create sequence folder
                seq_id = f"seq{sequence['id']:02d}"
                seq_path = cat_path / seq_id
                seq_path.mkdir(parents=True, exist_ok=True)
                
                # Create patterns within sequence
                for pattern_num in sequence['patterns']:
                    # Find pattern info
                    pattern_info = None
                    for p in category_info['patterns']:
                        if p['number'] == pattern_num:
                            pattern_info = p
                            break
                    
                    if pattern_info:
                        # Create pattern md
                        create_pattern_md(seq_path, pattern_num, pattern_info, dim_num)
                        
                        # Create pattern relations folder
                        create_pattern_relations_folder(seq_path, pattern_num, pattern_info)
    
    print("\n✓ Nested agency structure generated successfully!")
    print(f"Base path: {base_path}")

if __name__ == "__main__":
    generate_nested_structure()
