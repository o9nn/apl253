"""
NPU-253 Pattern Data Structures

Data classes for representing patterns and their metadata.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class PatternMetadata:
    """Metadata for a single APL pattern"""
    pattern_id: int
    name: str
    asterisks: int = 0
    category: str = ""  # "towns", "buildings", "construction"
    context: str = ""
    problem_summary: str = ""
    problem_details: str = ""
    solution: str = ""
    diagram: str = ""
    connections: str = ""
    preceding_patterns: List[int] = field(default_factory=list)
    following_patterns: List[int] = field(default_factory=list)
    sequence_memberships: List[int] = field(default_factory=list)


@dataclass
class ArchetypalPattern:
    """Archetypal pattern with domain transformations"""
    pattern_id: str
    name: str
    archetypal_pattern: str
    original_template: str = ""
    placeholders: List[str] = field(default_factory=list)
    domain_mappings: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    def transform_to_domain(self, domain: str) -> str:
        """
        Transform archetypal pattern to specific domain.
        
        Args:
            domain: One of "physical", "social", "conceptual", "psychic"
            
        Returns:
            Transformed pattern string with placeholders replaced
        """
        if domain not in ["physical", "social", "conceptual", "psychic"]:
            raise ValueError(f"Invalid domain: {domain}")
        
        result = self.archetypal_pattern
        
        # Replace each placeholder with domain-specific value
        for placeholder in self.placeholders:
            if placeholder in self.domain_mappings:
                domain_value = self.domain_mappings[placeholder].get(domain, f"{{placeholder}}")
                result = result.replace(f"{{{{{placeholder}}}}}", domain_value)
        
        return result


@dataclass
class PatternSequence:
    """A sequence of related patterns that work together"""
    sequence_id: int
    name: str
    description: str
    emergent_phenomena: str
    pattern_ids: List[int] = field(default_factory=list)


@dataclass
class PatternCategory:
    """Category grouping of patterns"""
    category_name: str  # "towns", "buildings", "construction"
    description: str
    pattern_range: tuple  # (start_id, end_id)
    pattern_ids: List[int] = field(default_factory=list)
