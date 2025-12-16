"""
NPU-253 Register Definitions

Memory-mapped I/O register addresses and command/status/error codes.
"""

# Base addresses
REG_BASE = 0x50000000
PATTERN_BASE = 0x50001000
ARCHETYPAL_BASE = 0x50100000

# Register offsets from REG_BASE
REG_CMD = 0x00              # Command register
REG_STATUS = 0x04           # Status flags
REG_PATTERN_ID = 0x08       # Current pattern ID (1-253)
REG_PATTERN_COUNT = 0x0C    # Total patterns loaded
REG_QUERY_ADDR = 0x10       # Address of query string (64-bit)
REG_QUERY_LEN = 0x18        # Length of query string
REG_RESULT_ADDR = 0x1C      # Address for results (64-bit)
REG_RESULT_COUNT = 0x24     # Number of matching patterns
REG_DOMAIN_MODE = 0x28      # Domain transformation mode
REG_SEQUENCE_ID = 0x2C      # Pattern sequence ID (1-36)
REG_CATEGORY = 0x30         # Category filter
REG_ERROR_CODE = 0x34       # Last error code
REG_PERF_QUERIES = 0x38     # Total queries processed
REG_PERF_TRANSFORMS = 0x3C  # Total transformations
REG_PERF_AVG_TIME_US = 0x40 # Average query time (microseconds)

# Command codes
CMD_RESET = 0x00           # Reset device state
CMD_LOAD_PATTERNS = 0x01   # Load all patterns into memory
CMD_QUERY_BY_ID = 0x02     # Query pattern by ID
CMD_QUERY_BY_NAME = 0x03   # Query pattern by name
CMD_QUERY_BY_TEXT = 0x04   # Full-text search
CMD_TRANSFORM = 0x05       # Apply domain transformation
CMD_GET_PRECEDING = 0x06   # Get preceding patterns
CMD_GET_FOLLOWING = 0x07   # Get following patterns
CMD_GET_SEQUENCE = 0x08    # Get pattern sequence
CMD_GET_CATEGORY = 0x09    # Get patterns by category
CMD_SELF_TEST = 0x0A       # Run self-diagnostics

# Status bits
STATUS_IDLE = 0x01            # Device ready for commands
STATUS_BUSY = 0x02            # Operation in progress
STATUS_READY = 0x04           # Results ready
STATUS_ERROR = 0x08           # Error occurred
STATUS_PATTERNS_LOADED = 0x10 # Patterns loaded into memory
STATUS_CACHE_HOT = 0x20       # Pattern cache warmed up
STATUS_SELF_TEST_OK = 0x40    # Self-test passed

# Error codes
ERR_NONE = 0x00              # No error
ERR_INVALID_CMD = 0x01       # Invalid command
ERR_PATTERN_NOT_FOUND = 0x02 # Pattern ID not found
ERR_INVALID_DOMAIN = 0x03    # Invalid domain mode
ERR_QUERY_TIMEOUT = 0x04     # Query timed out
ERR_TRANSFORM_FAIL = 0x05    # Transformation failed
ERR_MEMORY_ERROR = 0x06      # Memory access error
ERR_NOT_LOADED = 0x07        # Patterns not loaded

# Domain modes
DOMAIN_NONE = 0
DOMAIN_PHYSICAL = 1
DOMAIN_SOCIAL = 2
DOMAIN_CONCEPTUAL = 3
DOMAIN_PSYCHIC = 4

# Category codes
CATEGORY_ALL = 0
CATEGORY_TOWNS = 1
CATEGORY_BUILDINGS = 2
CATEGORY_CONSTRUCTION = 3
