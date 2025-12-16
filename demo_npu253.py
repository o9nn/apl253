#!/usr/bin/env python3
"""
NPU-253 Demo Application

Demonstrates the capabilities of the Neural Processing Unit / Natural Patterning Unit
virtual hardware device.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from npu253 import (
    PatternCoprocessorDriver,
    NPUConfig,
    CMD_LOAD_PATTERNS,
    CMD_SELF_TEST,
    STATUS_IDLE,
    STATUS_PATTERNS_LOADED,
)


def print_header(title: str) -> None:
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_operations(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate basic pattern operations"""
    print_header("Basic Pattern Operations")
    
    # Query by ID
    print("\n1. Query Pattern by ID (Pattern #1):")
    pattern = npu.query_by_id(1)
    if pattern:
        print(f"   Name: {pattern.name}")
        print(f"   Category: {pattern.category}")
        print(f"   Asterisks: {'*' * pattern.asterisks}")
        print(f"   Context: {pattern.context[:100]}...")
        print(f"   Solution: {pattern.solution[:150]}...")
    
    # Query by name
    print("\n2. Query Pattern by Name ('Sacred Sites'):")
    pattern = npu.query_by_name("Sacred Sites")
    if pattern:
        print(f"   Pattern ID: {pattern.pattern_id}")
        print(f"   Problem: {pattern.problem_summary[:100]}...")


def demo_text_search(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate full-text search"""
    print_header("Full-Text Search")
    
    search_terms = ["community", "light", "garden"]
    
    for term in search_terms:
        results = npu.query_by_text(term)
        print(f"\nSearching for '{term}': Found {len(results)} patterns")
        if results:
            print("   Top 3 results:")
            for p in results[:3]:
                print(f"   - Pattern {p.pattern_id}: {p.name}")


def demo_navigation(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate pattern relationship navigation"""
    print_header("Pattern Relationship Navigation")
    
    pattern_id = 1
    print(f"\nNavigating from Pattern {pattern_id}:")
    
    pattern = npu.query_by_id(pattern_id)
    if pattern:
        print(f"Pattern: {pattern.name}")
    
    # Get preceding patterns
    preceding = npu.get_preceding_patterns(pattern_id)
    print(f"\n  Preceding patterns ({len(preceding)}):")
    for p in preceding[:5]:
        print(f"    ← {p.pattern_id}: {p.name}")
    
    # Get following patterns
    following = npu.get_following_patterns(pattern_id)
    print(f"\n  Following patterns ({len(following)}):")
    for p in following[:5]:
        print(f"    → {p.pattern_id}: {p.name}")


def demo_categories(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate category queries"""
    print_header("Pattern Categories")
    
    categories = ["towns", "buildings", "construction"]
    
    for category in categories:
        patterns = npu.get_category(category)
        print(f"\n{category.upper()}: {len(patterns)} patterns")
        print(f"  Sample patterns:")
        for p in patterns[:3]:
            print(f"    - Pattern {p.pattern_id}: {p.name}")


def demo_sequences(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate pattern sequences"""
    print_header("Pattern Sequences")
    
    # Show first 3 sequences
    for seq_id in range(1, 4):
        patterns = npu.get_sequence(seq_id)
        if patterns:
            print(f"\nSequence {seq_id}: {len(patterns)} patterns")
            print(f"  Patterns: {', '.join(str(p.pattern_id) for p in patterns[:10])}")
            if len(patterns) > 10:
                print(f"            ... and {len(patterns) - 10} more")


def demo_domain_transformation(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate archetypal pattern domain transformation"""
    print_header("Domain Transformation (Archetypal Patterns)")
    
    # Get first archetypal pattern
    if not npu.archetypal_patterns:
        print("\n  No archetypal patterns loaded.")
        return
    
    pattern_id = list(npu.archetypal_patterns.keys())[0]
    pattern = npu.archetypal_patterns[pattern_id]
    
    print(f"\nArchetypal Pattern: {pattern.name}")
    print(f"Template: {pattern.archetypal_pattern[:100]}...")
    
    domains = ["physical", "social", "conceptual", "psychic"]
    
    for domain in domains:
        transformed = npu.transform_pattern(pattern_id, domain)
        if transformed:
            print(f"\n  {domain.upper()} domain:")
            print(f"    {transformed[:120]}...")


def demo_mmio_operations(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate low-level MMIO operations"""
    print_header("Low-Level MMIO Operations")
    
    print("\n1. Register Access:")
    
    # Read status register
    status = npu.read_reg32(0x04)
    print(f"   REG_STATUS (0x04): 0x{status:08X}")
    print(f"   Decoded: {npu.get_device_status()}")
    
    # Read pattern count
    count = npu.read_reg32(0x0C)
    print(f"   REG_PATTERN_COUNT (0x0C): {count} patterns")
    
    # Write and read pattern ID
    print("\n2. Pattern ID Register:")
    npu.write_reg32(0x08, 42)
    pattern_id = npu.read_reg32(0x08)
    print(f"   Set pattern ID to: {pattern_id}")
    
    # Read performance counters
    print("\n3. Performance Counters:")
    queries = npu.read_reg32(0x38)
    transforms = npu.read_reg32(0x3C)
    avg_time = npu.read_reg32(0x40)
    print(f"   Total queries: {queries}")
    print(f"   Total transforms: {transforms}")
    print(f"   Avg query time: {avg_time} μs")


def demo_telemetry(npu: PatternCoprocessorDriver) -> None:
    """Demonstrate telemetry and diagnostics"""
    print_header("Telemetry & Diagnostics")
    
    # Get telemetry
    print("\n1. Performance Telemetry:")
    telemetry = npu.get_telemetry()
    for key, value in telemetry.to_dict().items():
        print(f"   {key}: {value}")
    
    # Get device status
    print("\n2. Device Status:")
    print(f"   {npu.get_device_status()}")
    
    # Run self-test
    print("\n3. Self-Test:")
    if npu.run_self_test():
        print("   ✓ All self-tests passed")
    else:
        print("   ✗ Self-test failed")
    
    # Hardware diagnostics
    print("\n4. Full Hardware Diagnostics:")
    print(npu.get_hardware_diagnostics())


def main():
    """Main demo application"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                          NPU-253 Demo                                ║
║    Neural Processing Unit / Natural Patterning Unit                 ║
║                                                                      ║
║    Virtual Hardware Device for Pattern Language Processing          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize NPU-253
    print("\n[INIT] Initializing NPU-253 device driver...")
    config = NPUConfig(
        enable_cache=True,
        cache_size=128,
        enable_telemetry=True,
        verbose=False
    )
    
    npu = PatternCoprocessorDriver(config)
    
    # Probe device
    print("[PROBE] Probing device...")
    if not npu.probe():
        print("[ERROR] Device probe failed!")
        return 1
    print("[OK] Device detected")
    
    # Load patterns
    print("[LOAD] Loading patterns into device memory...")
    if not npu.load():
        print("[ERROR] Failed to load patterns!")
        return 1
    print(f"[OK] Loaded {len(npu.patterns)} APL patterns")
    print(f"[OK] Loaded {len(npu.archetypal_patterns)} archetypal patterns")
    
    # Initialize
    print("[INIT] Initializing device and running self-test...")
    if not npu.initialize():
        print("[ERROR] Device initialization failed!")
        return 1
    print("[OK] Device initialized and ready")
    
    # Run demos
    try:
        demo_basic_operations(npu)
        demo_text_search(npu)
        demo_navigation(npu)
        demo_categories(npu)
        demo_sequences(npu)
        demo_domain_transformation(npu)
        demo_mmio_operations(npu)
        demo_telemetry(npu)
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Demo interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n[ERROR] Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Cleanup
    print("\n" + "=" * 70)
    print("[CLEANUP] Removing device...")
    npu.remove()
    print("[OK] Device removed successfully")
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                       Demo Complete!                                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
