# NPU-253 API Documentation

## Overview

The NPU-253 (Neural Processing Unit / Natural Patterning Unit) provides a virtual hardware device interface for accelerated pattern language operations. This document describes the complete API for working with the NPU-253.

## Installation

```python
# The NPU-253 is part of the apl253 repository
import sys
sys.path.insert(0, '/path/to/apl253')

from npu253 import PatternCoprocessorDriver, NPUConfig
```

## Quick Start

```python
from npu253 import PatternCoprocessorDriver, NPUConfig

# Initialize with configuration
config = NPUConfig(
    enable_cache=True,
    cache_size=128,
    verbose=False
)

npu = PatternCoprocessorDriver(config)

# Load patterns
npu.load()

# Query a pattern
pattern = npu.query_by_id(1)
print(f"Pattern: {pattern.name}")
print(f"Solution: {pattern.solution}")

# Transform an archetypal pattern
transformed = npu.transform_pattern("12610010", "social")
print(f"Social domain: {transformed}")
```

## Configuration

### NPUConfig

```python
@dataclass
class NPUConfig:
    enable_cache: bool = True              # Enable pattern caching
    cache_size: int = 128                  # Maximum cache entries
    enable_telemetry: bool = True          # Enable performance tracking
    verbose: bool = False                  # Enable debug output
    pattern_data_path: str = "pattern_language_generated.json"
    archetypal_data_path: str = "archetypal_patterns.json"
    sequences_data_path: str = "pattern_sequences.json"
```

**Parameters:**
- `enable_cache`: Enable LRU caching for frequently accessed patterns
- `cache_size`: Maximum number of patterns to keep in cache
- `enable_telemetry`: Track performance metrics
- `verbose`: Print debug information to stdout
- `pattern_data_path`: Path to APL patterns JSON file
- `archetypal_data_path`: Path to archetypal patterns JSON file
- `sequences_data_path`: Path to pattern sequences JSON file

## Core Classes

### PatternCoprocessorDriver

Main driver class implementing the virtual hardware device.

#### Initialization

```python
driver = PatternCoprocessorDriver(config: Optional[NPUConfig] = None)
```

Creates a new NPU-253 device driver instance.

#### Device Lifecycle Methods

##### load()

```python
def load(self) -> bool
```

Loads patterns from JSON files into device memory.

**Returns:** `True` if successful, `False` otherwise

**Example:**
```python
if npu.load():
    print(f"Loaded {len(npu.patterns)} patterns")
```

##### initialize()

```python
def initialize(self) -> bool
```

Initializes device, warms up cache, and runs self-test.

**Returns:** `True` if initialization successful

**Example:**
```python
if npu.initialize():
    print("Device ready")
```

##### probe()

```python
def probe(self) -> bool
```

Probes device presence and capabilities.

**Returns:** `True` if device is accessible

##### remove()

```python
def remove(self) -> bool
```

Cleanup and remove device (clears all data).

**Returns:** `True` if successful

### Pattern Query Methods

##### query_by_id()

```python
def query_by_id(self, pattern_id: int) -> Optional[PatternMetadata]
```

Query pattern by ID (1-253).

**Parameters:**
- `pattern_id`: Pattern number (1-253)

**Returns:** `PatternMetadata` object or `None` if not found

**Example:**
```python
pattern = npu.query_by_id(1)
if pattern:
    print(f"Name: {pattern.name}")
    print(f"Category: {pattern.category}")
    print(f"Solution: {pattern.solution}")
```

##### query_by_name()

```python
def query_by_name(self, name: str) -> Optional[PatternMetadata]
```

Query pattern by name (case-insensitive).

**Parameters:**
- `name`: Pattern name to search for

**Returns:** `PatternMetadata` object or `None` if not found

**Example:**
```python
pattern = npu.query_by_name("Sacred Sites")
if pattern:
    print(f"Found pattern #{pattern.pattern_id}")
```

##### query_by_text()

```python
def query_by_text(self, text: str) -> List[PatternMetadata]
```

Full-text search across pattern content.

**Parameters:**
- `text`: Search string (case-insensitive)

**Returns:** List of matching patterns

**Example:**
```python
results = npu.query_by_text("community")
print(f"Found {len(results)} patterns containing 'community'")
for p in results:
    print(f"  - {p.pattern_id}: {p.name}")
```

### Pattern Navigation Methods

##### get_preceding_patterns()

```python
def get_preceding_patterns(self, pattern_id: int) -> List[PatternMetadata]
```

Get patterns that precede this pattern in the pattern language.

**Parameters:**
- `pattern_id`: Pattern ID to get predecessors for

**Returns:** List of preceding patterns

**Example:**
```python
preceding = npu.get_preceding_patterns(10)
print(f"Patterns before #10: {[p.pattern_id for p in preceding]}")
```

##### get_following_patterns()

```python
def get_following_patterns(self, pattern_id: int) -> List[PatternMetadata]
```

Get patterns that follow this pattern in the pattern language.

**Parameters:**
- `pattern_id`: Pattern ID to get successors for

**Returns:** List of following patterns

**Example:**
```python
following = npu.get_following_patterns(1)
print(f"Patterns after #1: {[p.pattern_id for p in following]}")
```

##### get_sequence()

```python
def get_sequence(self, sequence_id: int) -> List[PatternMetadata]
```

Get pattern sequence by ID (1-36).

**Parameters:**
- `sequence_id`: Sequence number (1-36)

**Returns:** List of patterns in the sequence

**Example:**
```python
sequence = npu.get_sequence(1)
print(f"Sequence 1 contains {len(sequence)} patterns")
for p in sequence:
    print(f"  {p.pattern_id}: {p.name}")
```

##### get_category()

```python
def get_category(self, category: str) -> List[PatternMetadata]
```

Get all patterns in a category.

**Parameters:**
- `category`: Category name ("towns", "buildings", or "construction")

**Returns:** List of patterns in the category

**Example:**
```python
towns = npu.get_category("towns")
print(f"Towns category has {len(towns)} patterns")
```

### Domain Transformation Methods

##### transform_pattern()

```python
def transform_pattern(self, pattern_id: str, domain: str) -> Optional[str]
```

Transform archetypal pattern to specific domain.

**Parameters:**
- `pattern_id`: Archetypal pattern ID (e.g., "12610010")
- `domain`: Target domain ("physical", "social", "conceptual", "psychic")

**Returns:** Transformed pattern string or `None` if error

**Example:**
```python
# Physical domain transformation
physical = npu.transform_pattern("12610010", "physical")
print(f"Physical: {physical}")

# Social domain transformation
social = npu.transform_pattern("12610010", "social")
print(f"Social: {social}")
```

### Low-Level MMIO Methods

##### write_reg32() / read_reg32()

```python
def write_reg32(self, offset: int, value: int) -> None
def read_reg32(self, offset: int) -> int
```

Write/read 32-bit values to/from registers.

**Example:**
```python
# Write pattern ID
npu.write_reg32(0x08, 42)

# Read status register
status = npu.read_reg32(0x04)
print(f"Status: 0x{status:08X}")
```

##### write_reg64() / read_reg64()

```python
def write_reg64(self, offset: int, value: int) -> None
def read_reg64(self, offset: int) -> int
```

Write/read 64-bit values to/from registers.

##### send_command()

```python
def send_command(self, cmd: int) -> bool
```

Send command to device.

**Parameters:**
- `cmd`: Command code (see register definitions)

**Returns:** `True` if successful

**Example:**
```python
from npu253 import CMD_SELF_TEST

npu.send_command(CMD_SELF_TEST)
```

##### wait_ready()

```python
def wait_ready(self, timeout_ms: int = 1000) -> bool
```

Wait for device ready status.

**Parameters:**
- `timeout_ms`: Timeout in milliseconds

**Returns:** `True` if device became ready, `False` on timeout

### Diagnostics Methods

##### run_self_test()

```python
def run_self_test(self) -> bool
```

Run comprehensive self-test.

**Returns:** `True` if all tests pass

**Example:**
```python
if npu.run_self_test():
    print("✓ Self-test passed")
else:
    print("✗ Self-test failed")
```

##### get_device_status()

```python
def get_device_status(self) -> str
```

Get human-readable device status string.

**Returns:** Status string (e.g., "IDLE | PATTERNS_LOADED | CACHE_HOT")

**Example:**
```python
print(f"Status: {npu.get_device_status()}")
```

##### get_telemetry()

```python
def get_telemetry(self) -> NPUTelemetry
```

Get performance telemetry data.

**Returns:** `NPUTelemetry` object

**Example:**
```python
telemetry = npu.get_telemetry()
print(f"Total queries: {telemetry.total_queries}")
print(f"Avg query time: {telemetry.avg_query_time_us} μs")
print(f"Cache hit rate: {telemetry.cache_hits / (telemetry.cache_hits + telemetry.cache_misses):.2%}")
```

##### get_hardware_diagnostics()

```python
def get_hardware_diagnostics(self) -> str
```

Get detailed hardware diagnostics report.

**Returns:** Multi-line diagnostics string

**Example:**
```python
print(npu.get_hardware_diagnostics())
```

## Data Structures

### PatternMetadata

```python
@dataclass
class PatternMetadata:
    pattern_id: int
    name: str
    asterisks: int
    category: str
    context: str
    problem_summary: str
    problem_details: str
    solution: str
    diagram: str
    connections: str
    preceding_patterns: List[int]
    following_patterns: List[int]
    sequence_memberships: List[int]
```

Represents a single APL pattern with all metadata.

**Example:**
```python
pattern = npu.query_by_id(1)
print(f"Pattern {pattern.pattern_id}: {pattern.name}")
print(f"Category: {pattern.category}")
print(f"Importance: {'*' * pattern.asterisks}")
print(f"Following patterns: {pattern.following_patterns}")
```

### ArchetypalPattern

```python
@dataclass
class ArchetypalPattern:
    pattern_id: str
    name: str
    archetypal_pattern: str
    original_template: str
    placeholders: List[str]
    domain_mappings: Dict[str, Dict[str, str]]
    
    def transform_to_domain(self, domain: str) -> str
```

Represents an archetypal pattern with domain transformation capabilities.

**Methods:**
- `transform_to_domain(domain)`: Transform to specific domain

**Example:**
```python
pattern = npu.archetypal_patterns["12610010"]
physical = pattern.transform_to_domain("physical")
social = pattern.transform_to_domain("social")
```

### NPUTelemetry

```python
@dataclass
class NPUTelemetry:
    total_queries: int
    total_transformations: int
    total_navigations: int
    avg_query_time_us: float
    cache_hits: int
    cache_misses: int
    uptime_seconds: float
    
    def to_dict(self) -> Dict
```

Performance telemetry data.

**Methods:**
- `to_dict()`: Convert to dictionary

## Register Definitions

### Register Offsets

```python
REG_CMD = 0x00              # Command register
REG_STATUS = 0x04           # Status flags
REG_PATTERN_ID = 0x08       # Current pattern ID
REG_PATTERN_COUNT = 0x0C    # Total patterns loaded
REG_QUERY_ADDR = 0x10       # Query string address (64-bit)
REG_QUERY_LEN = 0x18        # Query string length
REG_RESULT_ADDR = 0x1C      # Results address (64-bit)
REG_RESULT_COUNT = 0x24     # Number of results
REG_DOMAIN_MODE = 0x28      # Domain transformation mode
REG_SEQUENCE_ID = 0x2C      # Pattern sequence ID
REG_CATEGORY = 0x30         # Category filter
REG_ERROR_CODE = 0x34       # Last error code
REG_PERF_QUERIES = 0x38     # Total queries counter
REG_PERF_TRANSFORMS = 0x3C  # Total transformations counter
REG_PERF_AVG_TIME_US = 0x40 # Average query time (μs)
```

### Command Codes

```python
CMD_RESET = 0x00           # Reset device
CMD_LOAD_PATTERNS = 0x01   # Load patterns
CMD_QUERY_BY_ID = 0x02     # Query by ID
CMD_QUERY_BY_NAME = 0x03   # Query by name
CMD_QUERY_BY_TEXT = 0x04   # Full-text search
CMD_TRANSFORM = 0x05       # Domain transformation
CMD_GET_PRECEDING = 0x06   # Get preceding patterns
CMD_GET_FOLLOWING = 0x07   # Get following patterns
CMD_GET_SEQUENCE = 0x08    # Get pattern sequence
CMD_GET_CATEGORY = 0x09    # Get category
CMD_SELF_TEST = 0x0A       # Run self-test
```

### Status Bits

```python
STATUS_IDLE = 0x01            # Device ready
STATUS_BUSY = 0x02            # Operation in progress
STATUS_READY = 0x04           # Results ready
STATUS_ERROR = 0x08           # Error occurred
STATUS_PATTERNS_LOADED = 0x10 # Patterns loaded
STATUS_CACHE_HOT = 0x20       # Cache warmed up
STATUS_SELF_TEST_OK = 0x40    # Self-test passed
```

### Error Codes

```python
ERR_NONE = 0x00              # No error
ERR_INVALID_CMD = 0x01       # Invalid command
ERR_PATTERN_NOT_FOUND = 0x02 # Pattern not found
ERR_INVALID_DOMAIN = 0x03    # Invalid domain
ERR_QUERY_TIMEOUT = 0x04     # Query timeout
ERR_TRANSFORM_FAIL = 0x05    # Transformation failed
ERR_MEMORY_ERROR = 0x06      # Memory error
ERR_NOT_LOADED = 0x07        # Patterns not loaded
```

## Complete Examples

### Example 1: Basic Pattern Exploration

```python
from npu253 import PatternCoprocessorDriver, NPUConfig

# Initialize
config = NPUConfig(verbose=True)
npu = PatternCoprocessorDriver(config)
npu.load()

# Explore first pattern
pattern = npu.query_by_id(1)
print(f"Pattern 1: {pattern.name}")
print(f"Context: {pattern.context[:200]}...")
print(f"Solution: {pattern.solution[:200]}...")

# Navigate relationships
following = npu.get_following_patterns(1)
print(f"\nFollowing patterns:")
for p in following:
    print(f"  → {p.pattern_id}: {p.name}")
```

### Example 2: Category-Based Search

```python
# Get all building patterns
buildings = npu.get_category("buildings")
print(f"Found {len(buildings)} building patterns")

# Search within category
community_buildings = [
    p for p in buildings 
    if "community" in p.name.lower()
]

for p in community_buildings:
    print(f"{p.pattern_id}: {p.name}")
```

### Example 3: Domain Transformation Workflow

```python
# Get archetypal pattern
pattern_id = "12610010"
pattern = npu.archetypal_patterns[pattern_id]

print(f"Pattern: {pattern.name}")
print(f"Template: {pattern.archetypal_pattern}\n")

# Transform to all domains
domains = ["physical", "social", "conceptual", "psychic"]
for domain in domains:
    transformed = npu.transform_pattern(pattern_id, domain)
    print(f"{domain.upper()}:")
    print(f"  {transformed}\n")
```

### Example 4: Performance Monitoring

```python
import time

# Warm up
for i in range(1, 11):
    npu.query_by_id(i)

# Benchmark queries
start = time.time()
for i in range(1, 101):
    npu.query_by_id(i)
elapsed = time.time() - start

# Get telemetry
telemetry = npu.get_telemetry()
print(f"Queries: {telemetry.total_queries}")
print(f"Avg time: {telemetry.avg_query_time_us:.2f} μs")
print(f"Cache hit rate: {telemetry.cache_hits / (telemetry.cache_hits + telemetry.cache_misses):.2%}")
print(f"Total time: {elapsed:.3f} seconds")
print(f"QPS: {100 / elapsed:.2f}")
```

### Example 5: Low-Level Hardware Control

```python
from npu253 import CMD_QUERY_BY_ID, STATUS_READY

# Set pattern ID via register
npu.write_reg32(0x08, 42)

# Send query command
npu.send_command(CMD_QUERY_BY_ID)

# Wait for results
if npu.wait_ready(timeout_ms=100):
    result_count = npu.read_reg32(0x24)
    print(f"Query returned {result_count} results")
    
    # Get the pattern
    pattern = npu.query_by_id(42)
    if pattern:
        print(f"Found: {pattern.name}")
```

## Error Handling

```python
# Check for errors after operations
pattern = npu.query_by_id(9999)
if pattern is None:
    error_code = npu.read_reg32(0x34)
    if error_code == ERR_PATTERN_NOT_FOUND:
        print("Pattern not found")

# Check status flags
status = npu.read_reg32(0x04)
if status & STATUS_ERROR:
    error_code = npu.read_reg32(0x34)
    print(f"Error: 0x{error_code:02X}")
```

## Testing

Run the test suite:

```bash
python3 test_npu253.py
```

Run the demo application:

```bash
python3 demo_npu253.py
```

## Performance Considerations

1. **Caching**: Enable caching for frequently accessed patterns
2. **Batch Operations**: Query multiple patterns at once when possible
3. **Cache Size**: Adjust cache_size based on working set
4. **Telemetry**: Disable telemetry for maximum performance

```python
# High-performance configuration
config = NPUConfig(
    enable_cache=True,
    cache_size=256,        # Larger cache
    enable_telemetry=False, # Disable for speed
    verbose=False
)
```

## Thread Safety

The NPU-253 driver is **not thread-safe**. If using in a multi-threaded environment, use external synchronization:

```python
import threading

npu_lock = threading.Lock()

def safe_query(pattern_id):
    with npu_lock:
        return npu.query_by_id(pattern_id)
```

## See Also

- [NPU253_BLUEPRINT.md](NPU253_BLUEPRINT.md) - Architecture and design
- [demo_npu253.py](demo_npu253.py) - Demo application
- [test_npu253.py](test_npu253.py) - Test suite
