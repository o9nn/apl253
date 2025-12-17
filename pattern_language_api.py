#!/usr/bin/env python3
"""
Pattern Language Unified API

Integrates multiple components:
- Datalog query system (Phase 2)
- Salience scoring system (Phase 3)
- Pattern navigation and exploration

Provides a unified interface for optimal grip on the pattern language
gestalt salience landscape.
"""

from typing import Dict, List, Set, Optional, Tuple
from pathlib import Path
import json

from pattern_query_datalog import PatternQuerySystem
from pattern_salience_scorer import PatternSalienceScorer


class PatternLanguageAPI:
    """
    Unified API for Pattern Language operations.
    
    Integrates:
    - Declarative queries (Datalog)
    - Salience scoring (context, centrality, gestalt)
    - Pattern navigation
    - Cognitive affordances
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize unified API.
        
        Args:
            data_path: Path to pattern_language_generated.json
        """
        if data_path is None:
            data_path = str(Path("pattern_language_generated.json"))
        
        self.data_path = data_path
        self.query_system = PatternQuerySystem()
        self.salience_scorer = PatternSalienceScorer()
        
        # Load data
        self._load_data()
    
    def _load_data(self):
        """Load pattern data into both systems"""
        if Path(self.data_path).exists():
            # Load into query system
            self.query_system.load_from_json(self.data_path)
            
            # Load into salience scorer
            self.salience_scorer.load_from_json(self.data_path)
            
            # Load raw data for direct access
            with open(self.data_path, 'r') as f:
                self.data = json.load(f)
        else:
            raise FileNotFoundError(f"Pattern data not found: {self.data_path}")
    
    # Pattern Retrieval
    
    def get_pattern(self, pattern_id: str) -> Optional[Dict]:
        """
        Get a pattern by ID.
        
        Args:
            pattern_id: Pattern ID (e.g., 'apl1')
            
        Returns:
            Pattern dict or None if not found
        """
        return self.salience_scorer.patterns.get(pattern_id)
    
    def get_all_patterns(self) -> List[Dict]:
        """Get all patterns"""
        return list(self.salience_scorer.patterns.values())
    
    # Category Operations
    
    def get_categories(self) -> List[str]:
        """Get all pattern categories"""
        return self.query_system.query_all_categories()
    
    def get_patterns_in_category(self, category: str) -> List[str]:
        """Get all pattern IDs in a category"""
        return self.query_system.query_patterns_in_category(category)
    
    # Sequence Operations
    
    def get_sequences(self) -> List[str]:
        """Get all pattern sequences"""
        return self.query_system.query_all_sequences()
    
    def get_patterns_in_sequence(self, sequence_id: str) -> List[str]:
        """Get all pattern IDs in a sequence"""
        return self.query_system.query_patterns_in_sequence(sequence_id)
    
    def get_sequences_containing(self, pattern_id: str) -> List[str]:
        """Get all sequences containing a pattern"""
        return self.query_system.query_sequences_containing(pattern_id)
    
    # Relationship Queries
    
    def get_related_patterns(self, pattern_id: str) -> List[str]:
        """Get patterns related by category or sequence"""
        return self.query_system.query_related_patterns(pattern_id)
    
    def get_dependencies(self, pattern_id: str) -> List[str]:
        """Get all patterns this pattern depends on (transitively)"""
        return self.query_system.query_transitive_dependencies(pattern_id)
    
    def has_path(self, from_pattern: str, to_pattern: str) -> bool:
        """Check if there's a dependency path between patterns"""
        return self.query_system.find_pattern_path(from_pattern, to_pattern)
    
    # Context & Salience
    
    def rank_by_salience(
        self,
        context_keywords: Optional[List[str]] = None,
        active_patterns: Optional[Set[str]] = None,
        problem_forces: Optional[List[str]] = None,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Rank patterns by salience score.
        
        Args:
            context_keywords: Keywords describing context
            active_patterns: Currently active pattern IDs
            problem_forces: Problem forces/tensions
            top_k: Number of top patterns to return
            
        Returns:
            List of (pattern_id, score) tuples
        """
        return self.salience_scorer.rank_patterns(
            context_keywords=context_keywords,
            active_patterns=active_patterns,
            problem_forces=problem_forces,
            top_k=top_k
        )
    
    def compute_pattern_salience(
        self,
        pattern_id: str,
        context_keywords: Optional[List[str]] = None,
        active_patterns: Optional[Set[str]] = None,
        problem_forces: Optional[List[str]] = None
    ) -> float:
        """
        Compute salience score for a specific pattern.
        
        Args:
            pattern_id: Pattern to score
            context_keywords: Keywords describing context
            active_patterns: Currently active pattern IDs
            problem_forces: Problem forces/tensions
            
        Returns:
            Salience score [0, 1]
        """
        return self.salience_scorer.compute_salience(
            pattern_id,
            context_keywords=context_keywords,
            active_patterns=active_patterns,
            problem_forces=problem_forces
        )
    
    # Cognitive Affordances
    
    def get_pattern_context(self, pattern_id: str) -> Dict:
        """
        Get full context for a pattern including:
        - Basic info (name, number, category)
        - Relationships (sequences, related patterns)
        - Salience (centrality score)
        
        Args:
            pattern_id: Pattern ID
            
        Returns:
            Context dictionary
        """
        # Get basic context from query system
        context = self.query_system.get_pattern_context(pattern_id)
        
        # Add pattern details
        pattern = self.get_pattern(pattern_id)
        if pattern:
            context['number'] = pattern.get('number')
            context['asterisks'] = pattern.get('asterisks')
            context['problem'] = pattern.get('problem', '')[:200]  # Truncate
            context['solution'] = pattern.get('solution', '')[:200]
        
        # Add centrality score
        centrality = self.salience_scorer.compute_centrality()
        context['centrality'] = centrality.get(pattern_id, 0.0)
        
        return context
    
    def explore_from_pattern(
        self,
        pattern_id: str,
        context_keywords: Optional[List[str]] = None,
        max_related: int = 5
    ) -> Dict:
        """
        Explore pattern space starting from a pattern.
        
        Returns relevant patterns based on:
        - Category relationships
        - Sequence connections
        - Salience in given context
        
        Args:
            pattern_id: Starting pattern ID
            context_keywords: Optional context for salience
            max_related: Max related patterns to return
            
        Returns:
            Exploration results
        """
        # Get pattern context
        context = self.get_pattern_context(pattern_id)
        
        # Get related patterns
        related = self.get_related_patterns(pattern_id)[:max_related]
        
        # If context provided, rank by salience
        if context_keywords:
            active = {pattern_id}
            salient = self.rank_by_salience(
                context_keywords=context_keywords,
                active_patterns=active,
                top_k=max_related
            )
            related_salient = [(p, s) for p, s in salient if p in related]
        else:
            related_salient = [(p, 0.0) for p in related]
        
        return {
            'start_pattern': pattern_id,
            'pattern_name': context['name'],
            'category': context['category'],
            'sequences': context['sequences'],
            'related_patterns': [
                {
                    'id': pid,
                    'name': self.query_system.query_pattern_name(pid),
                    'salience': score
                }
                for pid, score in related_salient
            ],
            'dependencies': context['dependencies'][:max_related]
        }
    
    def find_pattern_clusters(self, min_size: int = 3) -> List[Set[str]]:
        """
        Find clusters of strongly connected patterns (gestalts).
        
        Args:
            min_size: Minimum cluster size
            
        Returns:
            List of pattern ID sets
        """
        return self.salience_scorer.find_pattern_clusters(min_size=min_size)
    
    def get_central_patterns(self, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Get most central patterns (structural importance).
        
        Args:
            top_k: Number of patterns to return
            
        Returns:
            List of (pattern_id, centrality_score) tuples
        """
        centrality = self.salience_scorer.compute_centrality()
        sorted_central = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_central[:top_k]
    
    # Search & Discovery
    
    def search_patterns(
        self,
        query: str,
        search_fields: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search patterns by text query.
        
        Args:
            query: Search query
            search_fields: Fields to search (default: name, problem, solution)
            max_results: Maximum results to return
            
        Returns:
            List of matching patterns with scores
        """
        if search_fields is None:
            search_fields = ['name', 'problem', 'solution']
        
        query_lower = query.lower()
        results = []
        
        for pattern in self.get_all_patterns():
            pid = pattern.get('id', '')
            
            # Search in specified fields
            text = ' '.join([
                str(pattern.get(field, '')).lower()
                for field in search_fields
            ])
            
            # Simple substring match with scoring
            if query_lower in text:
                # Count occurrences for scoring
                score = text.count(query_lower) / len(text.split())
                
                results.append({
                    'pattern_id': pid,
                    'name': pattern.get('name', ''),
                    'number': pattern.get('number', 0),
                    'category': [c for c in self.get_categories()
                               if pid in self.get_patterns_in_category(c)],
                    'score': score
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:max_results]
    
    # Statistics & Summaries
    
    def get_statistics(self) -> Dict:
        """Get overall pattern language statistics"""
        return {
            'total_patterns': len(self.salience_scorer.patterns),
            'categories': len(self.get_categories()),
            'sequences': len(self.get_sequences()),
            'graph_edges': self.salience_scorer.graph.number_of_edges(),
            'category_distribution': {
                cat: len(self.get_patterns_in_category(cat))
                for cat in self.get_categories()
            }
        }


def demo():
    """Demonstrate the unified API"""
    print("=" * 70)
    print("Pattern Language Unified API - Demo")
    print("Integration of Query System + Salience Scoring")
    print("=" * 70)
    print()
    
    # Initialize API
    api = PatternLanguageAPI()
    
    print("1. API Statistics")
    stats = api.get_statistics()
    print(f"   Total patterns: {stats['total_patterns']}")
    print(f"   Categories: {stats['categories']}")
    print(f"   Sequences: {stats['sequences']}")
    print(f"   Graph edges: {stats['graph_edges']}")
    print(f"   Category distribution:")
    for cat, count in stats['category_distribution'].items():
        print(f"     - {cat}: {count} patterns")
    print()
    
    print("2. Search Patterns")
    results = api.search_patterns('community', max_results=3)
    print(f"   Found {len(results)} patterns matching 'community':")
    for r in results:
        print(f"   - {r['pattern_id']}: {r['name']} (score: {r['score']:.4f})")
    print()
    
    print("3. Pattern Context")
    context = api.get_pattern_context('apl12')
    print(f"   Pattern: {context['name']}")
    print(f"   Category: {context['category']}")
    print(f"   Centrality: {context['centrality']:.4f}")
    print(f"   Sequences: {len(context['sequences'])}")
    print(f"   Related: {len(context['related'])}")
    print()
    
    print("4. Explore from Pattern")
    exploration = api.explore_from_pattern(
        'apl12',
        context_keywords=['neighborhood', 'housing'],
        max_related=3
    )
    print(f"   Starting from: {exploration['pattern_name']}")
    print(f"   Related patterns:")
    for p in exploration['related_patterns']:
        print(f"     - {p['id']}: {p['name']} (salience: {p['salience']:.4f})")
    print()
    
    print("5. Context-Based Ranking")
    top = api.rank_by_salience(
        context_keywords=['community', 'pedestrian', 'housing'],
        top_k=5
    )
    print("   Top 5 patterns for context ['community', 'pedestrian', 'housing']:")
    for pid, score in top:
        pattern = api.get_pattern(pid)
        print(f"   - {pid}: {pattern.get('name', '')} (score: {score:.4f})")
    print()
    
    print("6. Central Patterns")
    central = api.get_central_patterns(top_k=5)
    print("   Top 5 most central patterns:")
    for pid, score in central:
        pattern = api.get_pattern(pid)
        print(f"   - {pid}: {pattern.get('name', '')} (centrality: {score:.4f})")
    print()
    
    print("=" * 70)
    print("Demo complete!")
    print()
    print("Unified API provides:")
    print("  ✓ Pattern retrieval and search")
    print("  ✓ Category and sequence navigation")
    print("  ✓ Relationship queries (dependencies, related)")
    print("  ✓ Context-based salience ranking")
    print("  ✓ Pattern exploration and discovery")
    print("  ✓ Cognitive affordances (centrality, gestalts)")
    print("=" * 70)


if __name__ == '__main__':
    demo()
