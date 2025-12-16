#!/usr/bin/env python3
"""
Verify the nested agency structure in .github/agents/
"""

import os
from pathlib import Path

def verify_structure():
    """Verify the complete nested agency structure"""
    
    base_path = Path("/home/runner/work/apl253/apl253/.github/agents")
    
    # Check meta-pattern
    assert (base_path / "apl0.md").exists(), "Meta-pattern file apl0.md not found"
    print("✓ Meta-pattern file exists: apl0.md")
    
    # Check apl0 folder
    assert (base_path / "apl0").is_dir(), "apl0 folder not found"
    print("✓ Meta-pattern folder exists: apl0/")
    
    # Check dimensions
    dimensions = ["archetypal", "template", "physical", "social", "conceptual", "interpersonal"]
    for dim in dimensions:
        assert (base_path / "apl0" / f"{dim}.md").exists(), f"Dimension file {dim}.md not found"
        assert (base_path / "apl0" / dim).is_dir(), f"Dimension folder {dim}/ not found"
    print(f"✓ All {len(dimensions)} dimensions exist (files and folders)")
    
    # Check categories in each dimension
    categories = ["towns", "buildings", "construction"]
    for dim in dimensions:
        for cat in categories:
            dim_path = base_path / "apl0" / dim
            assert (dim_path / f"{cat}.md").exists(), f"Category file {cat}.md not found in {dim}"
            assert (dim_path / cat).is_dir(), f"Category folder {cat}/ not found in {dim}"
    print(f"✓ All {len(categories)} categories exist in each dimension (files and folders)")
    
    # Check sequences (36 total: 15 Towns, 13 Buildings, 8 Construction)
    sequence_counts = {
        "towns": 15,
        "buildings": 13,
        "construction": 8
    }
    
    for dim in dimensions:
        for cat, expected_count in sequence_counts.items():
            cat_path = base_path / "apl0" / dim / cat
            seq_folders = [d for d in cat_path.iterdir() if d.is_dir() and d.name.startswith("seq")]
            seq_files = [f for f in cat_path.iterdir() if f.is_file() and f.name.startswith("seq") and f.name.endswith(".md")]
            
            assert len(seq_folders) == expected_count, \
                f"Expected {expected_count} sequence folders in {dim}/{cat}, found {len(seq_folders)}"
            assert len(seq_files) == expected_count, \
                f"Expected {expected_count} sequence files in {dim}/{cat}, found {len(seq_files)}"
    
    print(f"✓ All 36 sequences exist in each dimension (15 Towns, 13 Buildings, 8 Construction)")
    
    # Check pattern files exist
    for dim in dimensions:
        pattern_files = list((base_path / "apl0" / dim).rglob("apl*.md"))
        # Should have many pattern files (patterns appear in sequences)
        assert len(pattern_files) > 250, f"Expected >250 pattern files in {dim}, found {len(pattern_files)}"
    
    print(f"✓ Pattern files exist in all dimensions")
    
    # Check sample pattern structure
    sample_pattern = base_path / "apl0" / "archetypal" / "towns" / "seq01" / "apl001.md"
    assert sample_pattern.exists(), "Sample pattern apl001.md not found"
    
    sample_relations = base_path / "apl0" / "archetypal" / "towns" / "seq01" / "apl001"
    assert sample_relations.is_dir(), "Sample pattern relations folder not found"
    
    print("✓ Sample pattern structure verified (apl001.md and relations folder)")
    
    # Summary statistics
    total_sequences = sum(len(list((base_path / "apl0" / dim / cat).glob("seq*.md"))) 
                         for dim in dimensions 
                         for cat in categories)
    
    total_pattern_files = len(list((base_path / "apl0").rglob("apl*.md")))
    
    total_relation_folders = len(list((base_path / "apl0").rglob("apl*"))) - total_pattern_files
    
    print("\n=== Summary Statistics ===")
    print(f"Meta-pattern files: 1 (apl0.md)")
    print(f"Dimensions: {len(dimensions)} (A, T, P, S, C, I)")
    print(f"Categories per dimension: {len(categories)} (Towns, Buildings, Construction)")
    print(f"Total sequences across all dimensions: {total_sequences} (should be {36 * len(dimensions)} = {36 * 6})")
    print(f"Total pattern files: {total_pattern_files}")
    print(f"Total relation folders: {total_relation_folders}")
    
    print("\n✓✓✓ All structure verification checks passed! ✓✓✓")

if __name__ == "__main__":
    verify_structure()
