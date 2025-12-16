"""
NPU-253: Neural Processing Unit / Natural Patterning Unit

A virtual hardware device implementing Christopher Alexander's 253-pattern 
language as a memory-mapped coprocessor.
"""

from .driver import PatternCoprocessorDriver
from .patterns import PatternMetadata, ArchetypalPattern
from .registers import (
    # Command codes
    CMD_RESET, CMD_LOAD_PATTERNS, CMD_QUERY_BY_ID, CMD_QUERY_BY_NAME,
    CMD_QUERY_BY_TEXT, CMD_TRANSFORM, CMD_GET_PRECEDING, CMD_GET_FOLLOWING,
    CMD_GET_SEQUENCE, CMD_GET_CATEGORY, CMD_SELF_TEST,
    
    # Status bits
    STATUS_IDLE, STATUS_BUSY, STATUS_READY, STATUS_ERROR,
    STATUS_PATTERNS_LOADED, STATUS_CACHE_HOT, STATUS_SELF_TEST_OK,
    
    # Error codes
    ERR_NONE, ERR_INVALID_CMD, ERR_PATTERN_NOT_FOUND, ERR_INVALID_DOMAIN,
    ERR_QUERY_TIMEOUT, ERR_TRANSFORM_FAIL, ERR_MEMORY_ERROR, ERR_NOT_LOADED,
    
    # Register offsets
    REG_CMD, REG_STATUS, REG_PATTERN_ID, REG_PATTERN_COUNT,
    REG_QUERY_ADDR, REG_QUERY_LEN, REG_RESULT_ADDR, REG_RESULT_COUNT,
    REG_DOMAIN_MODE, REG_SEQUENCE_ID, REG_CATEGORY, REG_ERROR_CODE,
    REG_PERF_QUERIES, REG_PERF_TRANSFORMS, REG_PERF_AVG_TIME_US
)
from .telemetry import NPUTelemetry, NPUConfig

__version__ = "1.0.0"
__all__ = [
    "PatternCoprocessorDriver",
    "PatternMetadata",
    "ArchetypalPattern",
    "NPUTelemetry",
    "NPUConfig",
    # Command codes
    "CMD_RESET", "CMD_LOAD_PATTERNS", "CMD_QUERY_BY_ID", "CMD_QUERY_BY_NAME",
    "CMD_QUERY_BY_TEXT", "CMD_TRANSFORM", "CMD_GET_PRECEDING", "CMD_GET_FOLLOWING",
    "CMD_GET_SEQUENCE", "CMD_GET_CATEGORY", "CMD_SELF_TEST",
    # Status bits
    "STATUS_IDLE", "STATUS_BUSY", "STATUS_READY", "STATUS_ERROR",
    "STATUS_PATTERNS_LOADED", "STATUS_CACHE_HOT", "STATUS_SELF_TEST_OK",
    # Error codes
    "ERR_NONE", "ERR_INVALID_CMD", "ERR_PATTERN_NOT_FOUND", "ERR_INVALID_DOMAIN",
    "ERR_QUERY_TIMEOUT", "ERR_TRANSFORM_FAIL", "ERR_MEMORY_ERROR", "ERR_NOT_LOADED",
]
