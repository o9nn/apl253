#!/usr/bin/env python3
"""
Pattern Language Datalog Query System - Phase 2 Implementation

This module implements the Datalog query layer over the OpenCog Atomese
representation to provide cognitive affordances for optimal grip on the
pattern language gestalt salience landscape.

Based on PARADIGM_LANGUAGE_ANALYSIS.md Phase 2 requirements.
"""

import json
import re
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
from pyDatalog import pyDatalog


# Initialize pyDatalog terms - must be done at module level
pyDatalog.create_terms('X, Y, Z, P, C, S, F, N')
pyDatalog.create_terms('pattern, category, sequence, force, name')
pyDatalog.create_terms('in_category, in_sequence, depends_on, has_force')
pyDatalog.create_terms('transitive_dep, same_category, connected_by_sequence')
pyDatalog.create_terms('related_patterns, pattern_path, has_name')


class PatternQuerySystem:
    """
    Datalog-based query system for Pattern Language.
    
    Implements Phase 2 of PARADIGM_LANGUAGE_ANALYSIS:
    - Declarative pattern queries
    - Relationship inference
    - Transitive dependencies
    - Multi-scale navigation
    """
    
    def __init__(self):
        """Initialize empty query system"""
        self.patterns = {}
        self.categories = set()
        self.sequences = set()
        self._define_inference_rules()
    
    def _define_inference_rules(self):
        """Define Datalog inference rules for pattern relationships"""
        
        # Rule 1: Transitive dependencies
        # If X depends on Y, and Y depends on Z, then X depends on Z
        transitive_dep(X, Y) <= depends_on(X, Y)
        transitive_dep(X, Z) <= (depends_on(X, Y) & transitive_dep(Y, Z))
        
        # Rule 2: Patterns in same category are related
        same_category(X, Y) <= (
            in_category(X, C) & 
            in_category(Y, C) & 
            (X != Y)
        )
        
        # Rule 3: Patterns in same sequence are connected
        connected_by_sequence(X, Y) <= (
            in_sequence(X, S) & 
            in_sequence(Y, S) & 
            (X != Y)
        )
        
        # Rule 4: Related patterns (by category or sequence)
        related_patterns(X, Y) <= same_category(X, Y)
        related_patterns(X, Y) <= connected_by_sequence(X, Y)
        
        # Rule 5: Pattern paths for navigation
        pattern_path(X, Y) <= transitive_dep(X, Y)
    
    def load_from_json(self, json_path: str) -> int:
        """
        Load patterns from JSON schema file.
        
        Args:
            json_path: Path to pattern_language_generated.json or similar
            
        Returns:
            Number of patterns loaded
            
        Note:
            This method calls pyDatalog.clear() which clears ALL facts from the
            global Datalog context. This may affect other PatternQuerySystem
            instances if used concurrently.
        """
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Clear existing facts (affects global Datalog context)
        pyDatalog.clear()
        self._define_inference_rules()
        
        fact_count = 0
        
        # Build category mapping from pattern numbers
        pattern_to_category = {}
        if 'categories' in data:
            for category in data['categories']:
                cat_name = category.get('name', '')
                pattern_range = category.get('pattern_range', {})
                start = pattern_range.get('start', 0)
                end = pattern_range.get('end', 0)
                
                # Map pattern numbers to category
                for num in range(start, end + 1):
                    pattern_to_category[num] = cat_name
                
                self.categories.add(cat_name)
        
        # Load patterns
        if 'patterns' in data:
            for pattern in data['patterns']:
                pid = pattern.get('id', '')
                self.patterns[pid] = pattern
                
                # Add name relation
                pname = pattern.get('name', '')
                if pname:
                    +has_name(pid, pname)
                    fact_count += 1
                
                # Add category membership based on pattern number
                pnumber = pattern.get('number', 0)
                if pnumber in pattern_to_category:
                    cat = pattern_to_category[pnumber]
                    +in_category(pid, cat)
                    fact_count += 1
                
                # Add forces (if they exist)
                forces = pattern.get('forces', [])
                for force in forces:
                    +has_force(pid, force)
                    fact_count += 1
                
                # Add dependencies from preceding patterns
                for prec_num in pattern.get('preceding_patterns', []):
                    prec_id = f"apl{prec_num}"
                    +depends_on(pid, prec_id)
                    fact_count += 1
        
        # Load sequences from categories
        if 'categories' in data:
            for category in data['categories']:
                for seq in category.get('sequences', []):
                    seq_id = f"Sequence-{seq.get('id', '')}"
                    self.sequences.add(seq_id)
                    
                    for pnumber in seq.get('patterns', []):
                        pid = f"apl{pnumber}"
                        +in_sequence(pid, seq_id)
                        fact_count += 1
        
        # Load meta-pattern dependencies
        if 'meta_pattern' in data:
            meta = data['meta_pattern']
            meta_id = meta.get('id', 'Pattern-0')
            
            for pid in meta.get('patterns', []):
                +depends_on(meta_id, pid)
                fact_count += 1
        
        return fact_count
    
    def load_from_atomese(self, scm_path: str) -> int:
        """
        Load facts from OpenCog Atomese .scm file.
        
        Args:
            scm_path: Path to .scm file
            
        Returns:
            Number of facts loaded
        """
        with open(scm_path, 'r') as f:
            content = f.read()
        
        fact_count = 0
        
        # Parse InheritanceLink -> in_category
        pattern = r'\(InheritanceLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(pattern, content):
            pid, cat = match.groups()
            +in_category(pid, cat)
            self.categories.add(cat)
            fact_count += 1
        
        # Parse MemberLink -> in_sequence
        pattern = r'\(MemberLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(pattern, content):
            pid, seq = match.groups()
            +in_sequence(pid, seq)
            self.sequences.add(seq)
            fact_count += 1
        
        # Parse ImplicationLink -> depends_on
        pattern = r'\(ImplicationLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(pattern, content):
            from_p, to_p = match.groups()
            +depends_on(from_p, to_p)
            fact_count += 1
        
        return fact_count
    
    # Query Methods
    
    def query_patterns_in_category(self, category: str) -> List[str]:
        """Find all patterns in a given category"""
        results = in_category(X, category)
        return sorted([str(x[0]) for x in results])
    
    def query_transitive_dependencies(self, pattern_id: str) -> List[str]:
        """Find all patterns that this pattern depends on (transitively)"""
        results = transitive_dep(pattern_id, X)
        return sorted([str(x[0]) for x in results])
    
    def query_related_patterns(self, pattern_id: str) -> List[str]:
        """Find patterns related by category or sequence"""
        results = related_patterns(pattern_id, X)
        return sorted([str(x[0]) for x in results])
    
    def query_patterns_in_sequence(self, sequence_id: str) -> List[str]:
        """Find all patterns in a sequence"""
        results = in_sequence(X, sequence_id)
        return sorted([str(x[0]) for x in results])
    
    def query_sequences_containing(self, pattern_id: str) -> List[str]:
        """Find all sequences containing a pattern"""
        results = in_sequence(pattern_id, X)
        return sorted([str(x[0]) for x in results])
    
    def query_patterns_with_force(self, force: str) -> List[str]:
        """Find patterns that address a specific force"""
        results = has_force(X, force)
        return sorted([str(x[0]) for x in results])
    
    def query_pattern_name(self, pattern_id: str) -> Optional[str]:
        """Get the name of a pattern"""
        results = has_name(pattern_id, X)
        return str(results[0][0]) if results else None
    
    def query_all_categories(self) -> List[str]:
        """Get all pattern categories"""
        return sorted(self.categories)
    
    def query_all_sequences(self) -> List[str]:
        """Get all pattern sequences"""
        return sorted(self.sequences)
    
    # Navigation Methods
    
    def find_pattern_path(self, from_pattern: str, to_pattern: str) -> bool:
        """Check if there's a dependency path from one pattern to another"""
        results = pattern_path(from_pattern, to_pattern)
        return len(results) > 0
    
    def get_pattern_context(self, pattern_id: str) -> Dict:
        """
        Get full context for a pattern:
        - Category
        - Sequences
        - Related patterns
        - Dependencies
        """
        return {
            'pattern_id': pattern_id,
            'name': self.query_pattern_name(pattern_id),
            'category': [c for c in self.categories 
                        if pattern_id in self.query_patterns_in_category(c)],
            'sequences': self.query_sequences_containing(pattern_id),
            'related': self.query_related_patterns(pattern_id)[:10],  # Top 10
            'dependencies': self.query_transitive_dependencies(pattern_id)[:10],
        }


def demo():
    """Demonstrate the Datalog query system"""
    print("=" * 70)
    print("Pattern Language Datalog Query System - Demo")
    print("Phase 2 Implementation: Query & Transformation")
    print("=" * 70)
    print()
    
    # Initialize system
    system = PatternQuerySystem()
    
    # Load data
    json_path = Path("pattern_language_generated.json")
    if json_path.exists():
        print(f"Loading patterns from {json_path}...")
        fact_count = system.load_from_json(str(json_path))
        print(f"✓ Loaded {fact_count} facts into Datalog")
        print(f"✓ Found {len(system.patterns)} patterns")
        print(f"✓ Found {len(system.categories)} categories")
        print(f"✓ Found {len(system.sequences)} sequences")
        print()
        
        # Demo queries
        print("1. Query: All pattern categories")
        categories = system.query_all_categories()
        print(f"   Found {len(categories)} categories:")
        for cat in categories[:5]:
            print(f"   - {cat}")
        if len(categories) > 5:
            print(f"   ... and {len(categories) - 5} more")
        print()
        
        print("2. Query: Patterns in 'Towns' category")
        towns = system.query_patterns_in_category('Towns')
        print(f"   Found {len(towns)} patterns:")
        for pid in towns[:5]:
            name = system.query_pattern_name(pid)
            print(f"   - {pid}: {name}")
        if len(towns) > 5:
            print(f"   ... and {len(towns) - 5} more")
        print()
        
        print("3. Query: All sequences")
        sequences = system.query_all_sequences()
        print(f"   Found {len(sequences)} sequences:")
        for seq in sequences[:5]:
            patterns = system.query_patterns_in_sequence(seq)
            print(f"   - {seq}: {len(patterns)} patterns")
        if len(sequences) > 5:
            print(f"   ... and {len(sequences) - 5} more")
        print()
        
        # Get a sample pattern for detailed queries
        if system.patterns:
            sample_pid = list(system.patterns.keys())[0]
            print(f"4. Query: Full context for '{sample_pid}'")
            context = system.get_pattern_context(sample_pid)
            print(f"   Name: {context['name']}")
            print(f"   Category: {context['category']}")
            print(f"   Sequences: {len(context['sequences'])}")
            print(f"   Related patterns: {len(context['related'])}")
            print(f"   Dependencies: {len(context['dependencies'])}")
            print()
        
        print("=" * 70)
        print("Demo complete!")
        print()
        print("Cognitive affordances provided:")
        print("  ✓ Multi-scale perception (categories, sequences)")
        print("  ✓ Relationship richness (multiple query types)")
        print("  ✓ Declarative queries (what, not how)")
        print("  ✓ Transitive inference (dependency chains)")
        print("  ✓ Fluid navigation (related patterns, paths)")
        print("=" * 70)
    else:
        print(f"✗ Pattern data file not found: {json_path}")
        print("  Please ensure pattern_language_generated.json exists")


if __name__ == '__main__':
    demo()
