# NPU-253: Neural Processing Unit / Natural Patterning Unit

## Executive Summary

The NPU-253 is a virtual hardware device that implements Christopher Alexander's 253-pattern language as a memory-mapped coprocessor. It treats pattern matching, domain transformation, and relationship navigation as hardware-accelerated operations accessible through MMIO (Memory-Mapped I/O) registers.

## Design Philosophy

**Hardware-First Thinking**: The pattern language system is conceptualized as a specialized processing unit with:
- Memory-mapped registers for control and status
- Pattern cache for rapid access
- Hardware-style command interface
- Telemetry and performance counters
- Self-diagnostic capabilities

**Pattern as Processing**: Each of the 253 patterns becomes a hardware-addressable entity with:
- Unique pattern ID (1-253)
- Register-mapped metadata
- Relationship pointers
- Domain transformation units

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       NPU-253 Architecture                   │
├─────────────────────────────────────────────────────────────┤
│  Control Interface (MMIO Registers @ 0x50000000)            │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ CMD Register │ Status Reg   │ Pattern ID   │            │
│  │ 0x50000000   │ 0x50000004   │ 0x50000008   │            │
│  └──────────────┴──────────────┴──────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Pattern Memory (253 Patterns @ 0x50001000)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Pattern[1..253]: Metadata, Relationships, Content    │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Processing Units                                           │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Query Engine │ Transform    │ Relationship │            │
│  │              │ Engine       │ Navigator    │            │
│  └──────────────┴──────────────┴──────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Archetypal Pattern Unit (102 Patterns @ 0x50100000)        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Domain Transformation: Physical/Social/Conceptual/   │  │
│  │ Psychic Mappings with Placeholder Engine             │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Telemetry & Diagnostics                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Performance Counters │ Health Metrics │ Error Logs   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Memory Map

### Control Registers (PERIPH Space @ 0x50000000)

| Offset | Register | Width | Description |
|--------|----------|-------|-------------|
| 0x00 | REG_CMD | 32-bit | Command register (load, query, transform, navigate) |
| 0x04 | REG_STATUS | 32-bit | Status flags (idle, busy, ready, error) |
| 0x08 | REG_PATTERN_ID | 32-bit | Current pattern ID (1-253) |
| 0x0C | REG_PATTERN_COUNT | 32-bit | Total patterns loaded (should be 253) |
| 0x10 | REG_QUERY_ADDR | 64-bit | Address of query string in SRAM |
| 0x18 | REG_QUERY_LEN | 32-bit | Length of query string |
| 0x1C | REG_RESULT_ADDR | 64-bit | Address for results |
| 0x24 | REG_RESULT_COUNT | 32-bit | Number of matching patterns |
| 0x28 | REG_DOMAIN_MODE | 32-bit | Domain transformation mode (0=none, 1=physical, 2=social, 3=conceptual, 4=psychic) |
| 0x2C | REG_SEQUENCE_ID | 32-bit | Pattern sequence ID (1-36) |
| 0x30 | REG_CATEGORY | 32-bit | Category filter (0=all, 1=towns, 2=buildings, 3=construction) |
| 0x34 | REG_ERROR_CODE | 32-bit | Last error code |
| 0x38 | REG_PERF_QUERIES | 32-bit | Total queries processed |
| 0x3C | REG_PERF_TRANSFORMS | 32-bit | Total transformations |
| 0x40 | REG_PERF_AVG_TIME_US | 32-bit | Average query time (microseconds) |

### Command Codes (REG_CMD)

```python
CMD_RESET           = 0x00  # Reset device state
CMD_LOAD_PATTERNS   = 0x01  # Load all patterns into memory
CMD_QUERY_BY_ID     = 0x02  # Query pattern by ID
CMD_QUERY_BY_NAME   = 0x03  # Query pattern by name
CMD_QUERY_BY_TEXT   = 0x04  # Full-text search
CMD_TRANSFORM       = 0x05  # Apply domain transformation
CMD_GET_PRECEDING   = 0x06  # Get preceding patterns
CMD_GET_FOLLOWING   = 0x07  # Get following patterns
CMD_GET_SEQUENCE    = 0x08  # Get pattern sequence
CMD_GET_CATEGORY    = 0x09  # Get patterns by category
CMD_SELF_TEST       = 0x0A  # Run self-diagnostics
```

### Status Bits (REG_STATUS)

```python
STATUS_IDLE         = 0x01  # Device ready for commands
STATUS_BUSY         = 0x02  # Operation in progress
STATUS_READY        = 0x04  # Results ready
STATUS_ERROR        = 0x08  # Error occurred
STATUS_PATTERNS_LOADED = 0x10  # Patterns loaded into memory
STATUS_CACHE_HOT    = 0x20  # Pattern cache warmed up
STATUS_SELF_TEST_OK = 0x40  # Self-test passed
```

### Error Codes (REG_ERROR_CODE)

```python
ERR_NONE            = 0x00  # No error
ERR_INVALID_CMD     = 0x01  # Invalid command
ERR_PATTERN_NOT_FOUND = 0x02  # Pattern ID not found
ERR_INVALID_DOMAIN  = 0x03  # Invalid domain mode
ERR_QUERY_TIMEOUT   = 0x04  # Query timed out
ERR_TRANSFORM_FAIL  = 0x05  # Transformation failed
ERR_MEMORY_ERROR    = 0x06  # Memory access error
ERR_NOT_LOADED      = 0x07  # Patterns not loaded
```

## Pattern Coprocessor Driver

### Core Data Structures

```python
@dataclass
class PatternMetadata:
    """Metadata for a single pattern"""
    pattern_id: int
    name: str
    asterisks: int
    category: str  # "towns", "buildings", "construction"
    context: str
    problem_summary: str
    solution: str
    preceding_patterns: List[int]
    following_patterns: List[int]
    sequence_memberships: List[int]

@dataclass
class ArchetypalPattern:
    """Archetypal pattern with domain transformations"""
    pattern_id: str
    name: str
    archetypal_template: str
    placeholders: List[str]
    domain_mappings: Dict[str, Dict[str, str]]
    
@dataclass
class NPUTelemetry:
    """Performance telemetry"""
    total_queries: int = 0
    total_transformations: int = 0
    total_navigations: int = 0
    avg_query_time_us: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    uptime_seconds: float = 0.0

@dataclass
class NPUConfig:
    """NPU-253 configuration"""
    enable_cache: bool = True
    cache_size: int = 128  # Number of patterns to cache
    enable_telemetry: bool = True
    verbose: bool = False
```

### Device Driver Interface

```python
class PatternCoprocessorDriver:
    """
    NPU-253 Pattern Coprocessor Driver
    
    Implements a virtual hardware device for accelerated pattern language
    operations with memory-mapped I/O interface.
    """
    
    # Memory-mapped register base addresses
    REG_BASE = 0x50000000
    PATTERN_BASE = 0x50001000
    ARCHETYPAL_BASE = 0x50100000
    
    def __init__(self, config: NPUConfig = None):
        """Initialize the NPU-253 device driver"""
        
    def load(self) -> bool:
        """Load patterns into device memory (hardware initialization)"""
        
    def initialize(self) -> bool:
        """Initialize device and run self-test"""
        
    def probe(self) -> bool:
        """Probe device presence and capabilities"""
        
    def remove(self) -> bool:
        """Cleanup and remove device"""
    
    # Low-level MMIO interface
    def write_reg32(self, offset: int, value: int) -> None:
        """Write 32-bit value to register"""
        
    def read_reg32(self, offset: int) -> int:
        """Read 32-bit value from register"""
        
    def write_reg64(self, offset: int, value: int) -> None:
        """Write 64-bit value to register"""
        
    def read_reg64(self, offset: int) -> int:
        """Read 64-bit value from register"""
    
    # Command interface
    def send_command(self, cmd: int) -> bool:
        """Send command to device"""
        
    def wait_ready(self, timeout_ms: int = 1000) -> bool:
        """Wait for device ready status"""
    
    # High-level pattern operations
    def query_by_id(self, pattern_id: int) -> Optional[PatternMetadata]:
        """Query pattern by ID (1-253)"""
        
    def query_by_name(self, name: str) -> Optional[PatternMetadata]:
        """Query pattern by name"""
        
    def query_by_text(self, text: str) -> List[PatternMetadata]:
        """Full-text search across patterns"""
        
    def transform_pattern(self, pattern_id: str, domain: str) -> str:
        """Transform archetypal pattern to specific domain"""
        
    def get_preceding_patterns(self, pattern_id: int) -> List[PatternMetadata]:
        """Get patterns that precede this pattern"""
        
    def get_following_patterns(self, pattern_id: int) -> List[PatternMetadata]:
        """Get patterns that follow this pattern"""
        
    def get_sequence(self, sequence_id: int) -> List[PatternMetadata]:
        """Get pattern sequence (1-36)"""
        
    def get_category(self, category: str) -> List[PatternMetadata]:
        """Get patterns by category (towns/buildings/construction)"""
    
    # Diagnostics and telemetry
    def run_self_test(self) -> bool:
        """Run comprehensive self-test"""
        
    def get_device_status(self) -> str:
        """Get human-readable device status"""
        
    def get_telemetry(self) -> NPUTelemetry:
        """Get performance telemetry"""
        
    def get_hardware_diagnostics(self) -> str:
        """Get detailed hardware diagnostics"""
```

## Implementation Phases

### Phase 1: Foundation (Current)
- ✅ Blueprint and architecture design
- ✅ Memory map definition
- ✅ Data structures
- 🔄 Base driver implementation

### Phase 2: Core Features
- Pattern loading from JSON files
- MMIO register simulation
- Basic query operations
- Status and error handling

### Phase 3: Advanced Features
- Domain transformation engine
- Relationship navigation
- Pattern sequences
- Full-text search

### Phase 4: Optimization
- Pattern caching
- Query optimization
- Performance telemetry
- Self-diagnostics

### Phase 5: Integration
- OpenCog Atomese bridge
- Demo applications
- Test suite
- Documentation

## Usage Examples

### Example 1: Basic Pattern Query

```python
from npu253 import PatternCoprocessorDriver, NPUConfig

# Initialize NPU-253
config = NPUConfig(enable_cache=True, verbose=True)
npu = PatternCoprocessorDriver(config)

# Load patterns (hardware initialization)
npu.load()
npu.initialize()

# Query pattern by ID
pattern = npu.query_by_id(1)
print(f"Pattern 1: {pattern.name}")
print(f"Category: {pattern.category}")
print(f"Solution: {pattern.solution[:100]}...")

# Get following patterns
following = npu.get_following_patterns(1)
print(f"Following patterns: {[p.pattern_id for p in following]}")
```

### Example 2: Domain Transformation

```python
# Transform archetypal pattern to social domain
archetypal_id = "12610010"
social_pattern = npu.transform_pattern(archetypal_id, "social")
print(f"Social domain pattern: {social_pattern}")

# Transform to conceptual domain
conceptual_pattern = npu.transform_pattern(archetypal_id, "conceptual")
print(f"Conceptual domain pattern: {conceptual_pattern}")
```

### Example 3: Pattern Sequence Navigation

```python
# Get a pattern sequence
sequence = npu.get_sequence(1)
print(f"Sequence 1 contains {len(sequence)} patterns:")
for p in sequence:
    print(f"  - Pattern {p.pattern_id}: {p.name}")
```

### Example 4: Full-Text Search

```python
# Search for patterns related to "community"
results = npu.query_by_text("community")
print(f"Found {len(results)} patterns containing 'community':")
for p in results[:5]:  # Top 5 results
    print(f"  - Pattern {p.pattern_id}: {p.name}")
```

### Example 5: Hardware-Style MMIO Control

```python
# Low-level register access
npu.write_reg32(0x08, 42)  # Set pattern ID to 42
pattern_id = npu.read_reg32(0x08)
print(f"Current pattern ID: {pattern_id}")

# Send command and wait
npu.send_command(CMD_QUERY_BY_ID)
if npu.wait_ready(timeout_ms=500):
    status = npu.read_reg32(0x04)
    if status & STATUS_READY:
        result_count = npu.read_reg32(0x24)
        print(f"Query returned {result_count} results")
```

### Example 6: Telemetry and Diagnostics

```python
# Get telemetry
telemetry = npu.get_telemetry()
print(f"Total queries: {telemetry.total_queries}")
print(f"Average query time: {telemetry.avg_query_time_us} μs")
print(f"Cache hit rate: {telemetry.cache_hits / (telemetry.cache_hits + telemetry.cache_misses):.2%}")

# Run self-test
if npu.run_self_test():
    print("✓ Self-test passed")
else:
    print("✗ Self-test failed")
    diagnostics = npu.get_hardware_diagnostics()
    print(diagnostics)
```

## Key Features

### 1. Hardware-Style Interface
- Memory-mapped registers for all control
- Status-driven state machine
- Hardware error codes
- Performance counters

### 2. Pattern Processing
- 253 APL patterns fully addressable
- 102 archetypal patterns with domain transformation
- 36 pattern sequences
- Full relationship graph navigation

### 3. Domain Transformation
- Physical domain (spatial, material)
- Social domain (organizational, community)
- Conceptual domain (knowledge, theoretical)
- Psychic domain (awareness, consciousness)

### 4. Performance & Telemetry
- Query performance tracking
- Cache hit/miss statistics
- Average operation times
- Uptime monitoring

### 5. Self-Diagnostics
- Comprehensive self-test
- Health checks
- Error reporting
- Status monitoring

## Integration Points

### OpenCog Atomese
The NPU-253 can serve as a hardware accelerator for OpenCog:
- Pattern queries translate to Atomese graph queries
- Relationship navigation uses hypergraph links
- Domain transformations generate Atomese variations

### Python Ecosystem
- JSON-based data interchange
- Standard Python typing
- Compatible with existing pattern generators
- Extensible driver architecture

## Future Enhancements

### Entelechy Framework
- Self-actualization metrics
- Ontogenetic evolution
- Fitness functions
- Autonomous optimization

### Advanced Processing
- Parallel pattern matching
- GPU acceleration (if available)
- Distributed pattern processing
- Real-time pattern synthesis

### AI/AGI Integration
- LLM-based pattern understanding
- Semantic similarity search
- Pattern generation from descriptions
- Meta-pattern discovery

## Technical Specifications

- **Language**: Python 3.8+
- **Data Format**: JSON
- **Memory Model**: Simulated MMIO with register dictionary
- **Pattern Count**: 253 APL + 102 Archetypal
- **Register Width**: 32/64-bit
- **Address Space**: 0x50000000 - 0x501FFFFF (2MB)

## Files to Create

1. `npu253/__init__.py` - Package initialization
2. `npu253/driver.py` - Main driver implementation
3. `npu253/registers.py` - Register definitions and constants
4. `npu253/patterns.py` - Pattern data structures
5. `npu253/telemetry.py` - Telemetry and diagnostics
6. `npu253/transform.py` - Domain transformation engine
7. `demo_npu253.py` - Demo application
8. `test_npu253.py` - Test suite
9. `NPU253_API.md` - API documentation

---

**Document Version**: 1.0  
**Date**: 2025-12-16  
**Status**: Blueprint Complete - Ready for Implementation
