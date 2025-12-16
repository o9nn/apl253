#!/usr/bin/env python3
"""
Pattern Language Query System - Datalog Integration Example

Demonstrates how to integrate Datalog queries with the existing OpenCog Atomese
implementation to achieve cognitive "optimal grip" on the pattern language.

This integrates:
- OpenCog Atomese (existing hypergraph)
- pyDatalog (declarative queries)
- NetworkX (graph analysis)
- Pattern salience computation
"""

import json
import re
from typing import List, Dict, Set, Tuple
from pyDatalog import pyDatalog

# Initialize pyDatalog terms
pyDatalog.create_terms('Pattern, Category, Sequence, X, Y, Z, P, C, S')
pyDatalog.create_terms('InCategory, InSequence, DependsOn, HasForce')
pyDatalog.create_terms('TransitiveDep, RelatedPatterns, PatternPath')
pyDatalog.create_terms('SameCategory, ConnectedBySequence')


class PatternLanguageQuerySystem:
    """
    Query system for Pattern Language using Datalog
    
    Provides cognitive affordances for:
    - Multi-scale perception (category hierarchies)
    - Relationship richness (multiple query types)
    - Contextual relevance (context-aware queries)
    - Emergence tracking (transitive relationships)
    """
    
    def __init__(self, pattern_json_path: str, atomese_path: str = None):
        """Initialize query system from pattern language JSON"""
        self.load_patterns(pattern_json_path)
        if atomese_path:
            self.load_atomese_facts(atomese_path)
        self.define_rules()
    
    def load_patterns(self, json_path: str):
        """Load patterns from JSON schema"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        self.patterns = {}
        
        # Load patterns
        if 'patterns' in data:
            for pattern in data['patterns']:
                pattern_id = pattern['id']
                self.patterns[pattern_id] = pattern
                
                # Add category membership
                if 'category' in pattern:
                    +InCategory(pattern_id, pattern['category'])
        
        # Load sequences
        if 'sequences' in data:
            for sequence in data['sequences']:
                seq_id = sequence['id']
                for pattern_id in sequence.get('patterns', []):
                    +InSequence(pattern_id, seq_id)
        
        # Load dependencies (from meta-pattern or pattern references)
        if 'meta_pattern' in data:
            meta = data['meta_pattern']
            meta_id = meta.get('id', 'Pattern-0')
            for pattern_id in meta.get('patterns', []):
                +DependsOn(meta_id, pattern_id)
        
        print(f"Loaded {len(self.patterns)} patterns into Datalog")
    
    def load_atomese_facts(self, scm_file: str):
        """Load facts from OpenCog Atomese .scm file"""
        with open(scm_file, 'r') as f:
            content = f.read()
        
        fact_count = 0
        
        # Parse InheritanceLink -> InCategory
        inheritance_pattern = r'\(InheritanceLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(inheritance_pattern, content):
            pattern_id, category = match.groups()
            +InCategory(pattern_id, category)
            fact_count += 1
        
        # Parse MemberLink -> InSequence
        member_pattern = r'\(MemberLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(member_pattern, content):
            pattern_id, sequence = match.groups()
            +InSequence(pattern_id, sequence)
            fact_count += 1
        
        # Parse ImplicationLink -> DependsOn
        implication_pattern = r'\(ImplicationLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
        for match in re.finditer(implication_pattern, content):
            from_pattern, to_pattern = match.groups()
            +DependsOn(from_pattern, to_pattern)
            fact_count += 1
        
        print(f"Loaded {fact_count} facts from Atomese")
    
    def define_rules(self):
        """Define Datalog inference rules"""
        
        # Rule 1: Transitive dependencies
        TransitiveDep(X, Y) <= DependsOn(X, Y)
        TransitiveDep(X, Z) <= (DependsOn(X, Y) & TransitiveDep(Y, Z))
        
        # Rule 2: Patterns in same category
        SameCategory(X, Y) <= (InCategory(X, C) & InCategory(Y, C) & (X != Y))
        
        # Rule 3: Patterns connected by sequence
        ConnectedBySequence(X, Y) <= (
            InSequence(X, S) & InSequence(Y, S) & (X != Y)
        )
        
        # Rule 4: Related patterns (same category OR connected by sequence)
        RelatedPatterns(X, Y) <= SameCategory(X, Y)
        RelatedPatterns(X, Y) <= ConnectedBySequence(X, Y)
        
        # Rule 5: Pattern path (for sequencing)
        PatternPath(X, Y) <= TransitiveDep(X, Y)
        
        print("Defined inference rules")
    
    def find_patterns_in_category(self, category: str) -> List[str]:
        """Find all patterns in a category"""
        results = InCategory(X, category)
        return sorted([str(x[0]) for x in results])
    
    def find_all_dependencies(self, pattern_id: str) -> List[str]:
        """Find all patterns this pattern depends on (transitively)"""
        results = TransitiveDep(pattern_id, X)
        return sorted([str(x[0]) for x in results])
    
    def find_dependents(self, pattern_id: str) -> List[str]:
        """Find all patterns that depend on this pattern"""
        results = TransitiveDep(X, pattern_id)
        return sorted([str(x[0]) for x in results])
    
    def find_related_patterns(self, pattern_id: str) -> Dict[str, List[str]]:
        """Find patterns related through category or sequence"""
        same_cat = SameCategory(pattern_id, X)
        connected_seq = ConnectedBySequence(pattern_id, X)
        
        return {
            'same_category': sorted([str(x[0]) for x in same_cat]),
            'connected_by_sequence': sorted([str(x[0]) for x in connected_seq])
        }
    
    def find_pattern_path(self, start: str, end: str) -> bool:
        """Check if there's a path from start to end pattern"""
        results = PatternPath(start, end)
        return len(list(results)) > 0
    
    def get_pattern_info(self, pattern_id: str) -> Dict:
        """Get comprehensive pattern information"""
        if pattern_id not in self.patterns:
            return None
        
        pattern = self.patterns[pattern_id]
        
        # Get relationships via queries
        dependencies = self.find_all_dependencies(pattern_id)
        dependents = self.find_dependents(pattern_id)
        related = self.find_related_patterns(pattern_id)
        
        # Get category
        categories = InCategory(pattern_id, X)
        category = str(list(categories)[0][0]) if categories else None
        
        # Get sequences
        sequences = InSequence(pattern_id, X)
        sequence_list = [str(x[0]) for x in sequences]
        
        return {
            'id': pattern_id,
            'name': pattern.get('name', ''),
            'category': category,
            'sequences': sequence_list,
            'dependencies': dependencies,
            'dependents': dependents,
            'related_patterns': related
        }
    
    def compute_pattern_centrality(self) -> Dict[str, float]:
        """
        Compute pattern centrality for salience
        
        Patterns with more dependencies/dependents are more central
        """
        centrality = {}
        
        for pattern_id in self.patterns:
            deps = len(self.find_all_dependencies(pattern_id))
            dependents = len(self.find_dependents(pattern_id))
            
            # Simple centrality: (dependencies + dependents) / 2
            centrality[pattern_id] = (deps + dependents) / 2
        
        # Normalize
        max_cent = max(centrality.values()) if centrality else 1
        if max_cent > 0:
            centrality = {k: v/max_cent for k, v in centrality.items()}
        
        return centrality
    
    def find_patterns_by_context(self, 
                                  domain: str = None,
                                  category: str = None,
                                  keywords: List[str] = None,
                                  active_patterns: Set[str] = None) -> List[Tuple[str, float]]:
        """
        Find patterns relevant to context (demonstrates contextual relevance)
        
        Returns list of (pattern_id, relevance_score) tuples
        """
        candidates = set(self.patterns.keys())
        scores = {}
        
        # Filter by category if specified
        if category:
            cat_patterns = set(self.find_patterns_in_category(category))
            candidates &= cat_patterns
        
        # Score each candidate
        for pattern_id in candidates:
            score = 0.0
            pattern = self.patterns[pattern_id]
            
            # Keyword matching
            if keywords:
                text = (pattern.get('name', '') + ' ' + 
                       pattern.get('problem', '') + ' ' +
                       pattern.get('solution', '')).lower()
                
                matches = sum(1 for kw in keywords if kw.lower() in text)
                score += 0.4 * (matches / len(keywords) if keywords else 0)
            
            # Centrality
            centrality = self.compute_pattern_centrality().get(pattern_id, 0)
            score += 0.3 * centrality
            
            # Connection to active patterns (emergence)
            if active_patterns:
                related = self.find_related_patterns(pattern_id)
                all_related = set(related['same_category']) | set(related['connected_by_sequence'])
                connections = len(all_related & active_patterns)
                score += 0.3 * (connections / len(active_patterns) if active_patterns else 0)
            
            scores[pattern_id] = score
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
    
    def generate_pattern_sequence(self, 
                                   goal_pattern: str,
                                   max_length: int = 10) -> List[str]:
        """
        Generate optimal pattern sequence to reach goal
        
        Uses transitive dependencies to find prerequisite patterns
        """
        # Find all prerequisites
        prerequisites = self.find_all_dependencies(goal_pattern)
        
        if not prerequisites:
            return [goal_pattern]
        
        # Build dependency graph to order them
        ordered = []
        remaining = set(prerequisites + [goal_pattern])
        
        while remaining and len(ordered) < max_length:
            # Find patterns with no remaining dependencies
            for pattern_id in list(remaining):
                deps = self.find_all_dependencies(pattern_id)
                deps_in_remaining = set(deps) & remaining
                
                if not deps_in_remaining or pattern_id in ordered:
                    ordered.append(pattern_id)
                    remaining.discard(pattern_id)
                    break
            else:
                # Circular dependency or stuck - just add remaining
                ordered.extend(remaining)
                break
        
        return ordered
    
    def detect_pattern_clusters(self) -> List[Set[str]]:
        """
        Detect clusters of highly related patterns (gestalts)
        
        Uses category and sequence membership to find tight groups
        """
        clusters = []
        visited = set()
        
        for pattern_id in self.patterns:
            if pattern_id in visited:
                continue
            
            # Find all related patterns
            cluster = {pattern_id}
            to_explore = {pattern_id}
            
            while to_explore:
                current = to_explore.pop()
                visited.add(current)
                
                related = self.find_related_patterns(current)
                neighbors = (set(related['same_category']) | 
                           set(related['connected_by_sequence']))
                
                new_neighbors = neighbors - cluster
                cluster.update(new_neighbors)
                to_explore.update(new_neighbors - visited)
            
            if len(cluster) >= 3:  # Only keep clusters of 3+ patterns
                clusters.append(cluster)
        
        return clusters


def demo_query_system():
    """Demonstrate the query system capabilities"""
    
    print("=" * 70)
    print("Pattern Language Query System - Datalog Integration Demo")
    print("=" * 70)
    print()
    
    # Initialize system
    print("1. Initializing system...")
    system = PatternLanguageQuerySystem('pattern_language_generated.json')
    print()
    
    # Demo 1: Category queries
    print("2. Demo: Find patterns in Towns category")
    towns_patterns = system.find_patterns_in_category('Category-Towns')
    print(f"   Found {len(towns_patterns)} patterns in Towns category")
    if towns_patterns:
        print(f"   First 5: {towns_patterns[:5]}")
    print()
    
    # Demo 2: Transitive dependencies
    print("3. Demo: Find dependencies of Pattern-0 (meta-pattern)")
    if 'Pattern-0' in system.patterns:
        deps = system.find_all_dependencies('Pattern-0')
        print(f"   Pattern-0 depends on {len(deps)} patterns (transitively)")
    print()
    
    # Demo 3: Related patterns
    print("4. Demo: Find patterns related to Pattern-42")
    if 'Pattern-42' in system.patterns:
        related = system.find_related_patterns('Pattern-42')
        print(f"   Same category: {len(related['same_category'])}")
        print(f"   Connected by sequence: {len(related['connected_by_sequence'])}")
    print()
    
    # Demo 4: Pattern info
    print("5. Demo: Get comprehensive pattern information")
    if 'Pattern-1' in system.patterns:
        info = system.get_pattern_info('Pattern-1')
        print(f"   Pattern: {info['name']}")
        print(f"   Category: {info['category']}")
        print(f"   # Dependencies: {len(info['dependencies'])}")
        print(f"   # Dependents: {len(info['dependents'])}")
    print()
    
    # Demo 5: Contextual search
    print("6. Demo: Find patterns by context")
    context_results = system.find_patterns_by_context(
        keywords=['community', 'public'],
        active_patterns={'Pattern-7', 'Pattern-28'}
    )
    print(f"   Top 5 relevant patterns:")
    for pattern_id, score in context_results[:5]:
        pattern = system.patterns.get(pattern_id, {})
        print(f"   - {pattern_id}: {pattern.get('name', '')} (score: {score:.3f})")
    print()
    
    # Demo 6: Pattern sequence generation
    print("7. Demo: Generate pattern sequence")
    if 'Pattern-42' in system.patterns:
        sequence = system.generate_pattern_sequence('Pattern-42', max_length=8)
        print(f"   Sequence to reach Pattern-42:")
        for i, pid in enumerate(sequence, 1):
            pattern = system.patterns.get(pid, {})
            print(f"   {i}. {pid}: {pattern.get('name', '')}")
    print()
    
    # Demo 7: Centrality analysis
    print("8. Demo: Pattern centrality (for salience)")
    centrality = system.compute_pattern_centrality()
    top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("   Top 5 most central patterns:")
    for pid, cent in top_central:
        pattern = system.patterns.get(pid, {})
        print(f"   - {pid}: {pattern.get('name', '')} (centrality: {cent:.3f})")
    print()
    
    # Demo 8: Pattern clusters (gestalts)
    print("9. Demo: Detect pattern clusters (gestalts)")
    clusters = system.detect_pattern_clusters()
    print(f"   Found {len(clusters)} pattern clusters")
    if clusters:
        print(f"   Largest cluster has {max(len(c) for c in clusters)} patterns")
    print()
    
    print("=" * 70)
    print("Demo complete! This demonstrates cognitive affordances:")
    print("  ✓ Multi-scale perception (categories, sequences)")
    print("  ✓ Relationship richness (multiple query types)")
    print("  ✓ Contextual relevance (context-aware search)")
    print("  ✓ Emergence tracking (transitive deps, clusters)")
    print("  ✓ Navigation support (related patterns, paths)")
    print("=" * 70)


if __name__ == '__main__':
    demo_query_system()
