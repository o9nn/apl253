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
    
    # Check dimensions (dim0-dim5)
    num_dimensions = 6
    for dim_num in range(num_dimensions):
        dim_name = f"dim{dim_num}"
        assert (base_path / "apl0" / f"{dim_name}.md").exists(), f"Dimension file {dim_name}.md not found"
        assert (base_path / "apl0" / dim_name).is_dir(), f"Dimension folder {dim_name}/ not found"
    print(f"✓ All {num_dimensions} dimensions exist (dim0-dim5 files and folders)")
    
    # Check categories in each dimension (cat1-cat3)
    num_categories = 3
    for dim_num in range(num_dimensions):
        dim_name = f"dim{dim_num}"
        for cat_num in range(1, num_categories + 1):
            cat_name = f"cat{cat_num}"
            dim_path = base_path / "apl0" / dim_name
            assert (dim_path / f"{cat_name}.md").exists(), f"Category file {cat_name}.md not found in {dim_name}"
            assert (dim_path / cat_name).is_dir(), f"Category folder {cat_name}/ not found in {dim_name}"
    print(f"✓ All {num_categories} categories exist in each dimension (cat1-cat3 files and folders)")
    
    # Check sequences (36 total: 15 cat1, 13 cat2, 8 cat3)
    sequence_counts = {
        "cat1": 15,
        "cat2": 13,
        "cat3": 8
    }
    
    for dim_num in range(num_dimensions):
        dim_name = f"dim{dim_num}"
        for cat_name, expected_count in sequence_counts.items():
            cat_path = base_path / "apl0" / dim_name / cat_name
            seq_folders = [d for d in cat_path.iterdir() if d.is_dir() and d.name.startswith("seq")]
            seq_files = [f for f in cat_path.iterdir() if f.is_file() and f.name.startswith("seq") and f.name.endswith(".md")]
            
            assert len(seq_folders) == expected_count, \
                f"Expected {expected_count} sequence folders in {dim_name}/{cat_name}, found {len(seq_folders)}"
            assert len(seq_files) == expected_count, \
                f"Expected {expected_count} sequence files in {dim_name}/{cat_name}, found {len(seq_files)}"
    
    print(f"✓ All 36 sequences exist in each dimension (15 cat1, 13 cat2, 8 cat3)")
    
    # Check pattern files exist
    for dim_num in range(num_dimensions):
        dim_name = f"dim{dim_num}"
        pattern_files = list((base_path / "apl0" / dim_name).rglob("apl*.md"))
        # Should have many pattern files (patterns appear in sequences)
        assert len(pattern_files) > 250, f"Expected >250 pattern files in {dim_name}, found {len(pattern_files)}"
    
    print(f"✓ Pattern files exist in all dimensions")
    
    # Check sample pattern structure
    sample_pattern = base_path / "apl0" / "dim0" / "cat1" / "seq01" / "apl001.md"
    assert sample_pattern.exists(), "Sample pattern apl001.md not found"
    
    sample_relations = base_path / "apl0" / "dim0" / "cat1" / "seq01" / "apl001"
    assert sample_relations.is_dir(), "Sample pattern relations folder not found"
    
    print("✓ Sample pattern structure verified (apl001.md and relations folder)")
    
    # Summary statistics
    total_sequences = 0
    for dim_num in range(num_dimensions):
        dim_name = f"dim{dim_num}"
        for cat_num in range(1, num_categories + 1):
            cat_name = f"cat{cat_num}"
            total_sequences += len(list((base_path / "apl0" / dim_name / cat_name).glob("seq*.md")))
    
    total_pattern_files = len(list((base_path / "apl0").rglob("apl*.md")))
    
    total_relation_folders = len(list((base_path / "apl0").rglob("apl*"))) - total_pattern_files
    
    print("\n=== Summary Statistics ===")
    print(f"Meta-pattern files: 1 (apl0.md)")
    print(f"Dimensions: {num_dimensions} (dim0-dim5)")
    print(f"Categories per dimension: {num_categories} (cat1-cat3)")
    print(f"Total sequences across all dimensions: {total_sequences} (should be {36 * num_dimensions} = {36 * 6})")
    print(f"Total pattern files: {total_pattern_files}")
    print(f"Total relation folders: {total_relation_folders}")
    
    print("\n✓✓✓ All structure verification checks passed! ✓✓✓")

if __name__ == "__main__":
    verify_structure()
