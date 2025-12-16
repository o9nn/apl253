#!/usr/bin/env python3
"""
Pattern Language Analysis - Basic Demo (No Dependencies)

Demonstrates pattern analysis capabilities without requiring external libraries.
Shows cognitive affordances for optimal grip on pattern language.
"""

import json
from typing import List, Dict, Set, Tuple
from collections import defaultdict


class BasicPatternAnalyzer:
    """
    Basic pattern analyzer demonstrating cognitive affordances
    
    Uses only Python standard library to show:
    - Multi-scale perception
    - Relationship richness
    - Contextual relevance
    - Pattern navigation
    """
    
    def __init__(self, pattern_json_path: str):
        """Initialize analyzer from pattern language JSON"""
        with open(pattern_json_path, 'r') as f:
            data = json.load(f)
        
        self.patterns = {}
        self.categories = defaultdict(set)
        self.sequences = defaultdict(set)
        self.dependencies = defaultdict(set)
        
        # Load patterns
        if 'patterns' in data:
            for pattern in data['patterns']:
                pattern_id = pattern['id']
                self.patterns[pattern_id] = pattern
                
                # Index by category
                if 'category' in pattern:
                    self.categories[pattern['category']].add(pattern_id)
        
        # Load sequences
        if 'sequences' in data:
            for sequence in data['sequences']:
                seq_id = sequence['id']
                for pattern_id in sequence.get('patterns', []):
                    self.sequences[seq_id].add(pattern_id)
        
        # Build dependency graph from meta-pattern
        if 'meta_pattern' in data:
            meta = data['meta_pattern']
            meta_id = meta.get('id', 'Pattern-0')
            for pattern_id in meta.get('patterns', []):
                self.dependencies[meta_id].add(pattern_id)
        
        print(f"✓ Loaded {len(self.patterns)} patterns")
        print(f"✓ Found {len(self.categories)} categories")
        print(f"✓ Found {len(self.sequences)} sequences")
    
    def get_patterns_in_category(self, category: str) -> List[str]:
        """Find all patterns in a category"""
        return sorted(list(self.categories.get(category, set())))
    
    def get_category_summary(self) -> Dict[str, int]:
        """Get pattern count per category"""
        return {cat: len(patterns) for cat, patterns in self.categories.items()}
    
    def get_sequence_summary(self) -> Dict[str, int]:
        """Get pattern count per sequence"""
        return {seq: len(patterns) for seq, patterns in self.sequences.items()}
    
    def find_patterns_by_keywords(self, keywords: List[str]) -> List[Tuple[str, int]]:
        """Find patterns matching keywords"""
        results = []
        
        for pattern_id, pattern in self.patterns.items():
            text = (
                pattern.get('name', '') + ' ' +
                pattern.get('problem', '') + ' ' +
                pattern.get('solution', '')
            ).lower()
            
            matches = sum(1 for kw in keywords if kw.lower() in text)
            if matches > 0:
                results.append((pattern_id, matches))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def analyze_pattern_connectivity(self) -> Dict[str, float]:
        """Analyze how connected each pattern is"""
        connectivity = {}
        
        for pattern_id in self.patterns:
            # Count category connections
            cat_connections = 0
            pattern_cat = None
            for cat, patterns in self.categories.items():
                if pattern_id in patterns:
                    pattern_cat = cat
                    cat_connections = len(patterns) - 1  # Exclude self
                    break
            
            # Count sequence connections
            seq_connections = 0
            for seq, patterns in self.sequences.items():
                if pattern_id in patterns:
                    seq_connections += len(patterns) - 1  # Exclude self
            
            # Total connectivity score
            connectivity[pattern_id] = cat_connections + seq_connections
        
        # Normalize to 0-1
        max_conn = max(connectivity.values()) if connectivity else 1
        if max_conn > 0:
            connectivity = {k: v/max_conn for k, v in connectivity.items()}
        
        return connectivity
    
    def get_multi_scale_view(self, pattern_id: str) -> Dict:
        """
        Get multi-scale view of a pattern
        Shows: individual pattern → category → full language
        """
        if pattern_id not in self.patterns:
            return None
        
        pattern = self.patterns[pattern_id]
        
        # Find category
        pattern_category = None
        category_patterns = []
        for cat, patterns in self.categories.items():
            if pattern_id in patterns:
                pattern_category = cat
                category_patterns = list(patterns)
                break
        
        # Find sequences
        pattern_sequences = []
        for seq, patterns in self.sequences.items():
            if pattern_id in patterns:
                pattern_sequences.append({
                    'sequence_id': seq,
                    'patterns_in_sequence': len(patterns)
                })
        
        return {
            'scale_1_individual': {
                'id': pattern_id,
                'name': pattern.get('name', ''),
                'problem_summary': pattern.get('problem', '')[:100] + '...'
            },
            'scale_2_category': {
                'category': pattern_category,
                'patterns_in_category': len(category_patterns),
                'sibling_patterns': category_patterns[:5]  # First 5
            },
            'scale_3_sequences': pattern_sequences,
            'scale_4_language': {
                'total_patterns': len(self.patterns),
                'total_categories': len(self.categories),
                'total_sequences': len(self.sequences)
            }
        }
    
    def find_related_patterns(self, pattern_id: str, context: Dict = None) -> List[Tuple[str, float, str]]:
        """
        Find patterns related to given pattern with relevance scores
        
        Returns: List of (pattern_id, relevance_score, relationship_type)
        """
        if pattern_id not in self.patterns:
            return []
        
        related = []
        
        # Find patterns in same category
        for cat, patterns in self.categories.items():
            if pattern_id in patterns:
                for other_id in patterns:
                    if other_id != pattern_id:
                        related.append((other_id, 0.6, 'same_category'))
        
        # Find patterns in same sequences
        for seq, patterns in self.sequences.items():
            if pattern_id in patterns:
                for other_id in patterns:
                    if other_id != pattern_id:
                        # Check if already added via category
                        existing = [r for r in related if r[0] == other_id]
                        if existing:
                            # Upgrade score
                            related.remove(existing[0])
                            related.append((other_id, 0.8, 'same_category_and_sequence'))
                        else:
                            related.append((other_id, 0.5, 'same_sequence'))
        
        # If context provided, boost patterns matching context
        if context and 'keywords' in context:
            keyword_matches = self.find_patterns_by_keywords(context['keywords'])
            keyword_pattern_ids = {pid for pid, _ in keyword_matches}
            
            for i, (rel_id, score, rel_type) in enumerate(related):
                if rel_id in keyword_pattern_ids:
                    related[i] = (rel_id, score + 0.2, rel_type + '_contextual')
        
        # Sort by relevance
        related.sort(key=lambda x: x[1], reverse=True)
        
        return related


def demo_basic_analyzer():
    """Demonstrate basic pattern analysis"""
    
    print("=" * 70)
    print("Pattern Language Analysis - Basic Demo")
    print("Demonstrating Cognitive Affordances for Optimal Grip")
    print("=" * 70)
    print()
    
    # Initialize
    print("1. Initializing Pattern Analyzer...")
    analyzer = BasicPatternAnalyzer('pattern_language_generated.json')
    print()
    
    # Demo 1: Multi-scale perception
    print("2. MULTI-SCALE PERCEPTION")
    print("   View pattern at different scales (individual → category → language)")
    print()
    
    if 'Pattern-42' in analyzer.patterns:
        multi_scale = analyzer.get_multi_scale_view('Pattern-42')
        
        print(f"   Scale 1 (Individual):")
        print(f"   - {multi_scale['scale_1_individual']['name']}")
        print()
        
        print(f"   Scale 2 (Category):")
        print(f"   - Category: {multi_scale['scale_2_category']['category']}")
        print(f"   - Patterns in category: {multi_scale['scale_2_category']['patterns_in_category']}")
        print()
        
        print(f"   Scale 3 (Sequences):")
        for seq in multi_scale['scale_3_sequences'][:2]:
            print(f"   - {seq['sequence_id']}: {seq['patterns_in_sequence']} patterns")
        print()
        
        print(f"   Scale 4 (Full Language):")
        print(f"   - Total patterns: {multi_scale['scale_4_language']['total_patterns']}")
        print(f"   - Total categories: {multi_scale['scale_4_language']['total_categories']}")
        print()
    
    # Demo 2: Category structure
    print("3. RELATIONSHIP RICHNESS")
    print("   Explore pattern categories and their sizes")
    print()
    
    category_summary = analyzer.get_category_summary()
    for cat, count in sorted(category_summary.items()):
        print(f"   - {cat}: {count} patterns")
    print()
    
    # Demo 3: Contextual search
    print("4. CONTEXTUAL RELEVANCE")
    print("   Find patterns by context keywords")
    print()
    
    keywords = ['community', 'public', 'gathering']
    print(f"   Keywords: {keywords}")
    print()
    
    results = analyzer.find_patterns_by_keywords(keywords)
    print(f"   Found {len(results)} relevant patterns")
    print("   Top 5:")
    for pattern_id, matches in results[:5]:
        pattern = analyzer.patterns[pattern_id]
        print(f"   - {pattern_id}: {pattern.get('name', '')} ({matches} keyword matches)")
    print()
    
    # Demo 4: Pattern connectivity
    print("5. EMERGENCE TRACKING")
    print("   Analyze pattern connectivity (gestalt formation potential)")
    print()
    
    connectivity = analyzer.analyze_pattern_connectivity()
    top_connected = sorted(connectivity.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print("   Top 5 most connected patterns:")
    for pattern_id, conn in top_connected:
        pattern = analyzer.patterns[pattern_id]
        print(f"   - {pattern_id}: {pattern.get('name', '')} (connectivity: {conn:.3f})")
    print()
    
    # Demo 5: Related patterns
    print("6. INTERACTIVE NAVIGATION")
    print("   Find patterns related to Pattern-42")
    print()
    
    if 'Pattern-42' in analyzer.patterns:
        context = {'keywords': ['community']}
        related = analyzer.find_related_patterns('Pattern-42', context)
        
        print(f"   Found {len(related)} related patterns")
        print("   Top 5:")
        for pattern_id, score, rel_type in related[:5]:
            pattern = analyzer.patterns[pattern_id]
            print(f"   - {pattern_id}: {pattern.get('name', '')} ({score:.2f}, {rel_type})")
    print()
    
    # Demo 6: Summary statistics
    print("7. GESTALT PERCEPTION")
    print("   Overall pattern language structure")
    print()
    
    total_patterns = len(analyzer.patterns)
    total_categories = len(analyzer.categories)
    total_sequences = len(analyzer.sequences)
    
    avg_patterns_per_category = total_patterns / total_categories if total_categories else 0
    
    print(f"   Total Patterns: {total_patterns}")
    print(f"   Categories: {total_categories}")
    print(f"   Sequences: {total_sequences}")
    print(f"   Avg patterns/category: {avg_patterns_per_category:.1f}")
    print()
    
    print("=" * 70)
    print("✓ Demo Complete!")
    print()
    print("Cognitive Affordances Demonstrated:")
    print("  ✓ Multi-scale perception (individual → category → language)")
    print("  ✓ Relationship richness (categories, sequences)")
    print("  ✓ Contextual relevance (keyword search)")
    print("  ✓ Emergence tracking (connectivity analysis)")
    print("  ✓ Interactive navigation (related patterns)")
    print("  ✓ Gestalt perception (structure overview)")
    print()
    print("For full capabilities, see:")
    print("  • demo_datalog_queries.py (requires pyDatalog)")
    print("  • IMPLEMENTATION_GUIDE.md (code examples)")
    print("  • OPTIMAL_GRIP_ANALYSIS.md (complete analysis)")
    print("=" * 70)


if __name__ == '__main__':
    demo_basic_analyzer()
