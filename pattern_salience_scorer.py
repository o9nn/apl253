#!/usr/bin/env python3
"""
Pattern Salience Scoring System - Phase 3 Implementation

This module implements cognitive salience scoring for patterns to achieve
"optimal grip" on the gestalt salience landscape. Salience scores help
identify which patterns are most relevant in a given context.

Based on PARADIGM_LANGUAGE_ANALYSIS.md Phase 3 requirements.
"""

import json
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path
from collections import defaultdict
import math


class PatternSalienceScorer:
    """
    Computes salience scores for patterns based on multiple factors:
    - Context relevance (semantic similarity)
    - Network centrality (structural importance)
    - Gestalt emergence (pattern combinations)
    - Force resonance (problem-solution fit)
    
    Implements Phase 3 of PARADIGM_LANGUAGE_ANALYSIS:
    - Context-based pattern relevance
    - Centrality analysis
    - Gestalt emergence detection
    """
    
    def __init__(self):
        """Initialize salience scorer"""
        self.patterns = {}
        self.graph = nx.DiGraph()
        self.category_index = defaultdict(list)
        self.sequence_index = defaultdict(list)
        self.force_index = defaultdict(list)
        self.centrality_cache = {}
    
    def load_from_json(self, json_path: str):
        """Load patterns from JSON file"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Build category mapping
        pattern_to_category = {}
        if 'categories' in data:
            for category in data['categories']:
                cat_name = category.get('name', '')
                pattern_range = category.get('pattern_range', {})
                start = pattern_range.get('start', 0)
                end = pattern_range.get('end', 0)
                
                for num in range(start, end + 1):
                    pattern_to_category[num] = cat_name
        
        # Load patterns and build graph
        if 'patterns' in data:
            for pattern in data['patterns']:
                pid = pattern.get('id', '')
                self.patterns[pid] = pattern
                self.graph.add_node(pid)
                
                # Index by category
                pnumber = pattern.get('number', 0)
                if pnumber in pattern_to_category:
                    cat = pattern_to_category[pnumber]
                    self.category_index[cat].append(pid)
                
                # Add edges from preceding patterns
                for prec_num in pattern.get('preceding_patterns', []):
                    prec_id = f"apl{prec_num}"
                    if prec_id in self.patterns or prec_num <= 253:
                        self.graph.add_edge(prec_id, pid)
                
                # Index by forces (if available)
                forces = pattern.get('forces', [])
                for force in forces:
                    self.force_index[force].append(pid)
        
        # Load sequences
        if 'categories' in data:
            for category in data['categories']:
                for seq in category.get('sequences', []):
                    seq_id = f"Sequence-{seq.get('id', '')}"
                    seq_patterns = [f"apl{num}" for num in seq.get('patterns', [])]
                    self.sequence_index[seq_id] = seq_patterns
                    
                    # Add sequence edges (patterns in sequence are connected)
                    for i, p1 in enumerate(seq_patterns):
                        for p2 in seq_patterns[i+1:]:
                            if not self.graph.has_edge(p1, p2):
                                self.graph.add_edge(p1, p2, weight=0.5)
    
    def compute_centrality(self) -> Dict[str, float]:
        """
        Compute network centrality for all patterns.
        Uses PageRank to identify structurally important patterns.
        """
        if not self.centrality_cache:
            try:
                self.centrality_cache = nx.pagerank(self.graph)
            except (nx.NetworkXException, nx.NetworkXError, ZeroDivisionError) as e:
                # Fallback to degree centrality if PageRank fails
                self.centrality_cache = nx.degree_centrality(self.graph)
        
        return self.centrality_cache
    
    def compute_betweenness_centrality(self) -> Dict[str, float]:
        """
        Compute betweenness centrality - patterns that bridge communities.
        """
        try:
            return nx.betweenness_centrality(self.graph)
        except (nx.NetworkXException, nx.NetworkXError, MemoryError) as e:
            # Return empty dict if computation fails
            return {}
    
    def compute_context_relevance(
        self, 
        pattern_id: str, 
        context_keywords: List[str]
    ) -> float:
        """
        Compute how relevant a pattern is to given context keywords.
        
        Args:
            pattern_id: Pattern to score
            context_keywords: List of keywords describing the context
            
        Returns:
            Relevance score [0, 1]
        """
        if pattern_id not in self.patterns:
            return 0.0
        
        pattern = self.patterns[pattern_id]
        
        # Get pattern text
        pattern_text = ' '.join([
            pattern.get('name', ''),
            pattern.get('problem', ''),
            pattern.get('solution', ''),
            pattern.get('context', '')
        ]).lower()
        
        # Count keyword matches
        matches = 0
        for keyword in context_keywords:
            if keyword.lower() in pattern_text:
                matches += 1
        
        # Normalize by number of keywords
        relevance = matches / len(context_keywords) if context_keywords else 0
        
        return min(relevance, 1.0)
    
    def compute_gestalt_score(
        self, 
        pattern_id: str, 
        active_patterns: Set[str]
    ) -> float:
        """
        Compute gestalt emergence score - how well pattern fits with
        currently active patterns.
        
        Args:
            pattern_id: Pattern to score
            active_patterns: Set of currently active pattern IDs
            
        Returns:
            Gestalt score [0, 1]
        """
        if pattern_id not in self.patterns:
            return 0.0
        
        # Score based on:
        # 1. Shared category with active patterns
        # 2. Shared sequences with active patterns
        # 3. Dependency relationships
        
        score = 0.0
        
        # Find pattern's category
        pattern_cats = [cat for cat, pats in self.category_index.items() 
                       if pattern_id in pats]
        
        # Count active patterns in same category
        category_overlap = 0
        for cat in pattern_cats:
            category_overlap += len([p for p in active_patterns 
                                    if p in self.category_index[cat]])
        
        # Count active patterns in same sequences
        sequence_overlap = 0
        for seq, pats in self.sequence_index.items():
            if pattern_id in pats:
                sequence_overlap += len([p for p in active_patterns if p in pats])
        
        # Count dependency relationships
        dependency_overlap = 0
        for active in active_patterns:
            if self.graph.has_edge(pattern_id, active):
                dependency_overlap += 1
            if self.graph.has_edge(active, pattern_id):
                dependency_overlap += 1
        
        # Combine scores
        if active_patterns:
            score = (
                (category_overlap * 0.3) +
                (sequence_overlap * 0.4) +
                (dependency_overlap * 0.3)
            ) / len(active_patterns)
        
        return min(score, 1.0)
    
    def compute_force_resonance(
        self, 
        pattern_id: str, 
        problem_forces: List[str]
    ) -> float:
        """
        Compute how well pattern addresses given problem forces.
        
        Args:
            pattern_id: Pattern to score
            problem_forces: List of forces/tensions in the problem
            
        Returns:
            Force resonance score [0, 1]
        """
        if pattern_id not in self.patterns:
            return 0.0
        
        pattern = self.patterns[pattern_id]
        
        # Get pattern forces (if available)
        pattern_forces = pattern.get('forces', [])
        
        # If no explicit forces, extract from problem/solution text
        if not pattern_forces:
            problem_text = pattern.get('problem', '').lower()
            solution_text = pattern.get('solution', '').lower()
            pattern_forces = [f for f in problem_forces 
                            if f.lower() in problem_text or f.lower() in solution_text]
        
        # Count force matches
        matches = 0
        for force in problem_forces:
            if force.lower() in [f.lower() for f in pattern_forces]:
                matches += 1
        
        resonance = matches / len(problem_forces) if problem_forces else 0
        return min(resonance, 1.0)
    
    def compute_salience(
        self,
        pattern_id: str,
        context_keywords: Optional[List[str]] = None,
        active_patterns: Optional[Set[str]] = None,
        problem_forces: Optional[List[str]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Compute overall salience score for a pattern.
        
        Args:
            pattern_id: Pattern to score
            context_keywords: Keywords describing current context
            active_patterns: Currently active pattern IDs
            problem_forces: Forces/tensions in current problem
            weights: Custom weights for different factors
            
        Returns:
            Overall salience score [0, 1]
        """
        if weights is None:
            weights = {
                'centrality': 0.2,
                'relevance': 0.3,
                'gestalt': 0.3,
                'force': 0.2
            }
        
        # Compute individual scores
        centrality = self.compute_centrality().get(pattern_id, 0.0)
        
        relevance = 0.0
        if context_keywords:
            relevance = self.compute_context_relevance(pattern_id, context_keywords)
        
        gestalt = 0.0
        if active_patterns:
            gestalt = self.compute_gestalt_score(pattern_id, active_patterns)
        
        force = 0.0
        if problem_forces:
            force = self.compute_force_resonance(pattern_id, problem_forces)
        
        # Weighted combination
        salience = (
            centrality * weights['centrality'] +
            relevance * weights['relevance'] +
            gestalt * weights['gestalt'] +
            force * weights['force']
        )
        
        return min(salience, 1.0)
    
    def rank_patterns(
        self,
        context_keywords: Optional[List[str]] = None,
        active_patterns: Optional[Set[str]] = None,
        problem_forces: Optional[List[str]] = None,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Rank all patterns by salience and return top K.
        
        Args:
            context_keywords: Keywords describing current context
            active_patterns: Currently active pattern IDs
            problem_forces: Forces/tensions in current problem
            top_k: Number of top patterns to return
            
        Returns:
            List of (pattern_id, salience_score) tuples, sorted by score
        """
        scores = []
        for pid in self.patterns:
            score = self.compute_salience(
                pid, 
                context_keywords, 
                active_patterns, 
                problem_forces
            )
            scores.append((pid, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]
    
    def find_pattern_clusters(self, min_size: int = 3) -> List[Set[str]]:
        """
        Find clusters of strongly connected patterns (gestalts).
        
        Args:
            min_size: Minimum cluster size
            
        Returns:
            List of pattern sets representing clusters
        """
        # Use community detection algorithm
        undirected = self.graph.to_undirected()
        
        try:
            import networkx.algorithms.community as nx_comm
            communities = nx_comm.greedy_modularity_communities(undirected)
            clusters = [set(c) for c in communities if len(c) >= min_size]
        except (ImportError, AttributeError, nx.NetworkXException) as e:
            # Fallback: use connected components if community detection fails
            clusters = [set(c) for c in nx.connected_components(undirected) 
                       if len(c) >= min_size]
        
        return clusters


def demo():
    """Demonstrate the salience scoring system"""
    print("=" * 70)
    print("Pattern Salience Scoring System - Demo")
    print("Phase 3 Implementation: Cognitive Enhancement")
    print("=" * 70)
    print()
    
    # Initialize scorer
    scorer = PatternSalienceScorer()
    
    # Load data
    json_path = Path("pattern_language_generated.json")
    if json_path.exists():
        print(f"Loading patterns from {json_path}...")
        scorer.load_from_json(str(json_path))
        print(f"✓ Loaded {len(scorer.patterns)} patterns")
        print(f"✓ Built graph with {scorer.graph.number_of_edges()} edges")
        print()
        
        # Demo 1: Network centrality
        print("1. Network Centrality Analysis")
        centrality = scorer.compute_centrality()
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("   Top 5 most central patterns (structural importance):")
        for pid, cent in top_central:
            pattern = scorer.patterns.get(pid, {})
            print(f"   - {pid}: {pattern.get('name', '')} (score: {cent:.4f})")
        print()
        
        # Demo 2: Context-based salience
        print("2. Context-Based Salience")
        context = ['community', 'neighborhood', 'housing', 'pedestrian']
        print(f"   Context keywords: {', '.join(context)}")
        top_relevant = scorer.rank_patterns(context_keywords=context, top_k=5)
        print("   Top 5 most relevant patterns:")
        for pid, score in top_relevant:
            pattern = scorer.patterns.get(pid, {})
            print(f"   - {pid}: {pattern.get('name', '')} (score: {score:.4f})")
        print()
        
        # Demo 3: Gestalt emergence
        print("3. Gestalt Emergence Score")
        active = {'apl12', 'apl13', 'apl14'}  # Some community patterns
        print(f"   Active patterns: {', '.join(sorted(active))}")
        
        # Find patterns with high gestalt score
        gestalt_scores = []
        for pid in scorer.patterns:
            if pid not in active:
                score = scorer.compute_gestalt_score(pid, active)
                if score > 0:
                    gestalt_scores.append((pid, score))
        
        gestalt_scores.sort(key=lambda x: x[1], reverse=True)
        print("   Top 5 patterns that fit with active patterns:")
        for pid, score in gestalt_scores[:5]:
            pattern = scorer.patterns.get(pid, {})
            print(f"   - {pid}: {pattern.get('name', '')} (score: {score:.4f})")
        print()
        
        # Demo 4: Pattern clusters (gestalts)
        print("4. Pattern Clusters (Gestalt Groups)")
        clusters = scorer.find_pattern_clusters(min_size=5)
        print(f"   Found {len(clusters)} pattern clusters")
        if clusters:
            largest = max(clusters, key=len)
            print(f"   Largest cluster has {len(largest)} patterns:")
            for pid in sorted(list(largest))[:5]:
                pattern = scorer.patterns.get(pid, {})
                print(f"   - {pid}: {pattern.get('name', '')}")
            if len(largest) > 5:
                print(f"   ... and {len(largest) - 5} more")
        print()
        
        print("=" * 70)
        print("Demo complete!")
        print()
        print("Cognitive affordances provided:")
        print("  ✓ Context-based relevance scoring")
        print("  ✓ Structural centrality analysis")
        print("  ✓ Gestalt emergence detection")
        print("  ✓ Pattern clustering")
        print("  ✓ Multi-factor salience computation")
        print("=" * 70)
    else:
        print(f"✗ Pattern data file not found: {json_path}")


if __name__ == '__main__':
    demo()
