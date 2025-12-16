#!/usr/bin/env python3
"""
Demo: Navigate the nested agency structure
"""

from pathlib import Path

def demo_navigation():
    """Demonstrate how to navigate the nested agency structure"""
    
    base = Path("/home/runner/work/apl253/apl253/.github/agents")
    
    print("=== NESTED AGENCY STRUCTURE NAVIGATION DEMO ===\n")
    
    # Level 0: Meta-pattern
    print("1. Start at Meta-Pattern Level:")
    print(f"   Read: {base}/apl0.md")
    meta = base / "apl0.md"
    if meta.exists():
        print(f"   ✓ Meta-pattern exists ({meta.stat().st_size} bytes)")
    
    # Level 1: Choose dimension
    print("\n2. Choose a Dimension (A, T, P, S, C, I):")
    dimensions = ["archetypal", "template", "physical", "social", "conceptual", "interpersonal"]
    for i, dim in enumerate(dimensions, 1):
        print(f"   {i}. {dim.title()}: {base}/apl0/{dim}.md")
    
    chosen_dim = "physical"
    print(f"\n   → Selected: {chosen_dim}")
    
    # Level 2: Choose category
    print("\n3. Choose a Category (1, 2, 3):")
    categories = {
        "1": ("towns", "Patterns 1-94, Sequences 01-15"),
        "2": ("buildings", "Patterns 95-204, Sequences 16-28"),
        "3": ("construction", "Patterns 205-253, Sequences 29-36")
    }
    for num, (name, desc) in categories.items():
        print(f"   {num}. {name.title()}: {desc}")
        print(f"      {base}/apl0/{chosen_dim}/{name}.md")
    
    chosen_cat = "buildings"
    print(f"\n   → Selected: {chosen_cat}")
    
    # Level 3: Choose sequence
    print("\n4. Choose a Sequence (16-28 for buildings):")
    seq_path = base / "apl0" / chosen_dim / chosen_cat
    sequences = sorted([d.name for d in seq_path.iterdir() if d.is_dir() and d.name.startswith("seq")])
    print(f"   Available sequences: {', '.join(sequences[:5])}, ...")
    
    chosen_seq = "seq20"
    print(f"\n   → Selected: {chosen_seq}")
    print(f"   Read: {seq_path}/{chosen_seq}.md")
    
    # Level 4: View patterns in sequence
    print("\n5. View Patterns in Sequence:")
    pattern_path = seq_path / chosen_seq
    patterns = sorted([f.stem for f in pattern_path.iterdir() if f.is_file() and f.name.endswith(".md")])
    print(f"   Patterns in {chosen_seq}: {', '.join(patterns[:5])}, ...")
    
    chosen_pattern = "apl132"
    print(f"\n   → Selected: {chosen_pattern}")
    print(f"   Read: {pattern_path}/{chosen_pattern}.md")
    
    # Level 5: View pattern relations
    print("\n6. View Pattern Relations:")
    relations_path = pattern_path / chosen_pattern
    if relations_path.exists():
        relations = [f.name for f in relations_path.iterdir() if f.is_file()]
        for rel in relations:
            print(f"   - {relations_path}/{rel}")
    
    # Summary
    print("\n=== NAVIGATION PATH ===")
    full_path = f"apl0 → {chosen_dim} → {chosen_cat} → {chosen_seq} → {chosen_pattern}"
    print(f"   {full_path}")
    print(f"\n   Full path: .github/agents/apl0/{chosen_dim}/{chosen_cat}/{chosen_seq}/{chosen_pattern}.md")
    
    # Cross-dimensional navigation
    print("\n=== CROSS-DIMENSIONAL EXPLORATION ===")
    print(f"To view the same pattern in different dimensions:")
    for dim in ["archetypal", "social", "conceptual"]:
        cross_path = f"apl0/{dim}/{chosen_cat}/{chosen_seq}/{chosen_pattern}.md"
        full_cross = base / cross_path
        if full_cross.exists():
            print(f"   ✓ {cross_path}")
    
    print("\n✓ Demo complete!")

if __name__ == "__main__":
    demo_navigation()
