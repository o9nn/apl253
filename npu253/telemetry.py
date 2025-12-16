"""
NPU-253 Telemetry and Configuration

Performance monitoring and configuration structures.
"""

from dataclasses import dataclass, field
from typing import Dict
import time


@dataclass
class NPUConfig:
    """NPU-253 configuration"""
    enable_cache: bool = True
    cache_size: int = 128  # Number of patterns to cache
    enable_telemetry: bool = True
    verbose: bool = False
    pattern_data_path: str = "pattern_language_generated.json"
    archetypal_data_path: str = "archetypal_patterns.json"
    sequences_data_path: str = "pattern_sequences.json"


@dataclass
class NPUTelemetry:
    """Performance telemetry and statistics"""
    total_queries: int = 0
    total_transformations: int = 0
    total_navigations: int = 0
    avg_query_time_us: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    uptime_seconds: float = 0.0
    start_time: float = field(default_factory=time.time)
    
    # Per-operation timing
    query_times: list = field(default_factory=list)
    transform_times: list = field(default_factory=list)
    
    def update_uptime(self) -> None:
        """Update uptime calculation"""
        self.uptime_seconds = time.time() - self.start_time
    
    def record_query_time(self, time_us: float) -> None:
        """Record a query execution time"""
        self.query_times.append(time_us)
        self.total_queries += 1
        
        # Update rolling average
        if len(self.query_times) > 1000:
            self.query_times = self.query_times[-1000:]  # Keep last 1000
        self.avg_query_time_us = sum(self.query_times) / len(self.query_times)
    
    def record_transform_time(self, time_us: float) -> None:
        """Record a transformation execution time"""
        self.transform_times.append(time_us)
        self.total_transformations += 1
        
        # Keep rolling window
        if len(self.transform_times) > 1000:
            self.transform_times = self.transform_times[-1000:]
    
    def to_dict(self) -> Dict:
        """Convert telemetry to dictionary"""
        self.update_uptime()
        return {
            "total_queries": self.total_queries,
            "total_transformations": self.total_transformations,
            "total_navigations": self.total_navigations,
            "avg_query_time_us": round(self.avg_query_time_us, 2),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": round(self.cache_hits / max(1, self.cache_hits + self.cache_misses), 4),
            "uptime_seconds": round(self.uptime_seconds, 2),
        }
