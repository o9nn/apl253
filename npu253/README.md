# NPU-253: Neural Processing Unit / Natural Patterning Unit

The NPU-253 is a virtual hardware device that implements Christopher Alexander's 253-pattern language as a memory-mapped coprocessor. It provides hardware-style MMIO registers for accelerated pattern operations including querying, domain transformation, and relationship navigation.

## Features

- **Hardware-Style Interface**: Memory-mapped I/O registers for all control operations
- **253 APL Patterns**: Complete Christopher Alexander "A Pattern Language" dataset
- **253 Archetypal Patterns**: Domain-transformable patterns (physical/social/conceptual/psychic)
- **36 Pattern Sequences**: Pre-defined pattern sequences with emergent phenomena
- **Pattern Navigation**: Traverse preceding/following pattern relationships
- **Domain Transformation**: Transform archetypal patterns across domains
- **LRU Caching**: Configurable pattern cache for performance
- **Telemetry & Diagnostics**: Comprehensive performance monitoring
- **Self-Testing**: Built-in hardware diagnostics

## Quick Start

```python
from npu253 import PatternCoprocessorDriver, NPUConfig

# Initialize NPU-253
config = NPUConfig(enable_cache=True, cache_size=128)
npu = PatternCoprocessorDriver(config)

# Load patterns
npu.load()

# Query a pattern
pattern = npu.query_by_id(1)
print(f"{pattern.name}: {pattern.solution[:100]}...")

# Transform archetypal pattern
social = npu.transform_pattern("12610010", "social")
print(f"Social domain: {social}")
```

## Memory Map

```
0x50000000 - Control Registers (PERIPH space)
  0x00 - CMD        Command register
  0x04 - STATUS     Status flags
  0x08 - PATTERN_ID Current pattern ID
  0x0C - PATTERN_COUNT Total patterns
  0x10 - QUERY_ADDR Query string address
  0x18 - QUERY_LEN  Query length
  0x1C - RESULT_ADDR Results address
  0x24 - RESULT_COUNT Result count
  0x28 - DOMAIN_MODE Domain transformation mode
  0x2C - SEQUENCE_ID Pattern sequence ID
  0x30 - CATEGORY   Category filter
  0x34 - ERROR_CODE Last error
  0x38 - PERF_QUERIES Performance counter
  0x3C - PERF_TRANSFORMS Transform counter
  0x40 - PERF_AVG_TIME_US Average query time

0x50001000 - Pattern Memory (253 APL patterns)
0x50100000 - Archetypal Pattern Memory (253 patterns)
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│               PatternCoprocessorDriver              │
├─────────────────────────────────────────────────────┤
│  Control Interface (MMIO Registers)                 │
│  ┌──────────┬──────────┬──────────┬──────────┐     │
│  │   CMD    │  STATUS  │PATTERN_ID│  ERROR   │     │
│  └──────────┴──────────┴──────────┴──────────┘     │
├─────────────────────────────────────────────────────┤
│  Pattern Storage                                    │
│  ┌─────────────────────────────────────────────┐   │
│  │ 253 APL Patterns                            │   │
│  │ 253 Archetypal Patterns                     │   │
│  │ 36 Pattern Sequences                        │   │
│  │ 3 Categories (Towns/Buildings/Construction) │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  Processing Units                                   │
│  ┌─────────┬─────────────┬────────────────┐        │
│  │ Query   │ Transform   │ Navigation     │        │
│  │ Engine  │ Engine      │ Engine         │        │
│  └─────────┴─────────────┴────────────────┘        │
├─────────────────────────────────────────────────────┤
│  Performance Layer                                  │
│  ┌─────────┬─────────────┬────────────────┐        │
│  │ LRU     │ Telemetry   │ Diagnostics    │        │
│  │ Cache   │             │                │        │
│  └─────────┴─────────────┴────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## Module Structure

```
npu253/
├── __init__.py       # Package initialization, exports
├── driver.py         # Main PatternCoprocessorDriver class
├── patterns.py       # Pattern data structures
├── registers.py      # Register and command definitions
└── telemetry.py      # Telemetry and configuration
```

## API Overview

### Device Lifecycle

```python
npu = PatternCoprocessorDriver(config)
npu.load()        # Load patterns
npu.initialize()  # Initialize and self-test
npu.probe()       # Check device presence
npu.remove()      # Cleanup
```

### Pattern Queries

```python
# Query by ID
pattern = npu.query_by_id(1)

# Query by name
pattern = npu.query_by_name("Sacred Sites")

# Full-text search
results = npu.query_by_text("community")
```

### Pattern Navigation

```python
# Get relationships
preceding = npu.get_preceding_patterns(10)
following = npu.get_following_patterns(1)

# Get sequences
sequence = npu.get_sequence(1)

# Get by category
towns = npu.get_category("towns")
buildings = npu.get_category("buildings")
construction = npu.get_category("construction")
```

### Domain Transformation

```python
# Transform to specific domains
physical = npu.transform_pattern("12610010", "physical")
social = npu.transform_pattern("12610010", "social")
conceptual = npu.transform_pattern("12610010", "conceptual")
psychic = npu.transform_pattern("12610010", "psychic")
```

### Low-Level MMIO

```python
# Register access
npu.write_reg32(0x08, 42)  # Write pattern ID
pattern_id = npu.read_reg32(0x08)

# Command interface
npu.send_command(CMD_SELF_TEST)
npu.wait_ready(timeout_ms=1000)
```

### Diagnostics

```python
# Self-test
npu.run_self_test()

# Get status
status = npu.get_device_status()

# Get telemetry
telemetry = npu.get_telemetry()
print(f"Queries: {telemetry.total_queries}")
print(f"Avg time: {telemetry.avg_query_time_us} μs")

# Hardware diagnostics
print(npu.get_hardware_diagnostics())
```

## Testing

Run the comprehensive test suite:

```bash
python3 test_npu253.py
```

**Test Coverage:**
- ✅ Register operations (32-bit and 64-bit)
- ✅ Pattern loading and initialization
- ✅ Pattern queries (by ID, name, text)
- ✅ Pattern navigation (preceding, following)
- ✅ Categories and sequences
- ✅ Domain transformation
- ✅ Caching (LRU)
- ✅ Telemetry tracking
- ✅ Self-diagnostics
- ✅ Command interface

**Result:** 34/34 tests passing ✅

## Demo Application

Run the demo to see all features:

```bash
python3 demo_npu253.py
```

The demo showcases:
- Basic pattern operations
- Full-text search
- Pattern relationship navigation
- Category queries
- Pattern sequences
- Domain transformation
- Low-level MMIO operations
- Telemetry and diagnostics

## Performance

Typical performance on standard hardware:

- **Query by ID**: ~100 μs (cache hit: ~10 μs)
- **Query by name**: ~500 μs
- **Full-text search**: ~1-5 ms (depends on corpus size)
- **Domain transformation**: ~200 μs
- **Pattern navigation**: ~100 μs

Cache hit rate typically >90% for repeated queries.

## Configuration

```python
config = NPUConfig(
    enable_cache=True,      # Enable LRU cache
    cache_size=128,         # Cache up to 128 patterns
    enable_telemetry=True,  # Track performance
    verbose=False,          # Debug output
    pattern_data_path="pattern_language_generated.json",
    archetypal_data_path="archetypal_patterns.json",
    sequences_data_path="pattern_sequences.json"
)
```

## Data Structures

### PatternMetadata

Complete pattern metadata including:
- Pattern ID, name, category
- Context, problem, solution
- Diagram and connections
- Preceding/following patterns
- Sequence memberships

### ArchetypalPattern

Domain-transformable patterns with:
- Template with placeholders
- Domain mappings (physical/social/conceptual/psychic)
- Transform method

### NPUTelemetry

Performance metrics:
- Query/transformation counts
- Average operation times
- Cache statistics
- Uptime

## Documentation

- **[NPU253_BLUEPRINT.md](../NPU253_BLUEPRINT.md)** - Complete architecture and design
- **[NPU253_API.md](../NPU253_API.md)** - Full API reference with examples
- **[demo_npu253.py](../demo_npu253.py)** - Comprehensive demo application
- **[test_npu253.py](../test_npu253.py)** - Complete test suite

## Design Philosophy

The NPU-253 treats the pattern language system as a **virtual hardware device**:

1. **Hardware-First**: Everything exposed through MMIO registers
2. **Status-Driven**: Hardware status bits drive operation
3. **Memory-Mapped**: Pattern data accessible through memory regions
4. **Performance-Oriented**: Caching, telemetry, optimization
5. **Diagnostic-Rich**: Self-testing and comprehensive diagnostics

This approach enables:
- Hardware-style abstraction of pattern operations
- Integration with other virtual devices
- Clear separation of concerns
- High performance through caching
- Detailed observability

## Future Enhancements

- Entelechy framework (self-actualization metrics)
- Ontogenetic evolution (self-optimization)
- OpenCog Atomese integration
- Parallel pattern processing
- GPU acceleration
- Distributed pattern operations
- Pattern synthesis and generation

## License

See [LICENSE](../LICENSE) in the repository root.

## Credits

- **Pattern Language**: Christopher Alexander et al., "A Pattern Language" (1977)
- **UIA Patterns**: Union of International Associations
- **NPU-253 Design**: Virtual hardware device implementation (2025)
