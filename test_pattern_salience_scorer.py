#!/usr/bin/env python3
"""
Tests for Pattern Salience Scoring System

Tests Phase 3 implementation: Cognitive Enhancement
"""

import pytest
from pathlib import Path
from pattern_salience_scorer import PatternSalienceScorer


@pytest.fixture
def salience_scorer():
    """Create and initialize salience scorer"""
    scorer = PatternSalienceScorer()
    json_path = Path("pattern_language_generated.json")
    
    if json_path.exists():
        scorer.load_from_json(str(json_path))
    else:
        pytest.skip("pattern_language_generated.json not found")
    
    return scorer


class TestPatternSalienceScorer:
    """Test suite for PatternSalienceScorer"""
    
    def test_initialization(self, salience_scorer):
        """Test scorer initialization"""
        assert salience_scorer is not None
        assert len(salience_scorer.patterns) > 0
        assert salience_scorer.graph.number_of_nodes() > 0
        assert salience_scorer.graph.number_of_edges() > 0
    
    def test_load_patterns(self, salience_scorer):
        """Test pattern loading"""
        assert len(salience_scorer.patterns) == 253
        assert 'apl1' in salience_scorer.patterns
        assert 'apl253' in salience_scorer.patterns
    
    def test_category_index(self, salience_scorer):
        """Test category indexing"""
        assert len(salience_scorer.category_index) == 3
        assert 'Towns' in salience_scorer.category_index
        assert len(salience_scorer.category_index['Towns']) == 94
    
    def test_sequence_index(self, salience_scorer):
        """Test sequence indexing"""
        assert len(salience_scorer.sequence_index) == 36
        assert 'Sequence-1' in salience_scorer.sequence_index
        assert len(salience_scorer.sequence_index['Sequence-1']) > 0
    
    def test_compute_centrality(self, salience_scorer):
        """Test centrality computation"""
        centrality = salience_scorer.compute_centrality()
        
        assert len(centrality) > 0
        assert all(0 <= score <= 1 for score in centrality.values())
        
        # Check that results are cached
        centrality2 = salience_scorer.compute_centrality()
        assert centrality == centrality2
    
    def test_compute_betweenness_centrality(self, salience_scorer):
        """Test betweenness centrality computation"""
        betweenness = salience_scorer.compute_betweenness_centrality()
        
        if betweenness:  # May be empty if graph has issues
            assert all(0 <= score <= 1 for score in betweenness.values())
    
    def test_compute_context_relevance(self, salience_scorer):
        """Test context relevance computation"""
        # Test with relevant keywords
        score = salience_scorer.compute_context_relevance(
            'apl12', 
            ['community', 'neighborhood']
        )
        assert 0 <= score <= 1
        assert score > 0  # Should have some relevance
        
        # Test with irrelevant keywords
        score2 = salience_scorer.compute_context_relevance(
            'apl12',
            ['zzz', 'xxx', 'www']
        )
        assert score2 == 0  # Should have no relevance
        
        # Test with empty keywords
        score3 = salience_scorer.compute_context_relevance('apl12', [])
        assert score3 == 0
    
    def test_compute_gestalt_score(self, salience_scorer):
        """Test gestalt emergence score computation"""
        # Test with related active patterns
        active = {'apl12', 'apl13', 'apl14'}
        score = salience_scorer.compute_gestalt_score('apl15', active)
        assert 0 <= score <= 1
        assert score > 0  # Should have some gestalt score
        
        # Test with empty active patterns
        score2 = salience_scorer.compute_gestalt_score('apl15', set())
        assert score2 == 0
        
        # Test with unrelated active patterns
        active2 = {'apl250', 'apl251', 'apl252'}
        score3 = salience_scorer.compute_gestalt_score('apl1', active2)
        assert 0 <= score3 <= 1
    
    def test_compute_force_resonance(self, salience_scorer):
        """Test force resonance computation"""
        # Test with problem forces
        score = salience_scorer.compute_force_resonance(
            'apl12',
            ['community', 'social', 'connection']
        )
        assert 0 <= score <= 1
        
        # Test with empty forces
        score2 = salience_scorer.compute_force_resonance('apl12', [])
        assert score2 == 0
    
    def test_compute_salience_basic(self, salience_scorer):
        """Test basic salience computation"""
        score = salience_scorer.compute_salience('apl12')
        assert 0 <= score <= 1
        assert score > 0  # Should have some base salience
    
    def test_compute_salience_with_context(self, salience_scorer):
        """Test salience with context keywords"""
        score = salience_scorer.compute_salience(
            'apl12',
            context_keywords=['community', 'neighborhood']
        )
        assert 0 <= score <= 1
        assert score > 0
    
    def test_compute_salience_with_active_patterns(self, salience_scorer):
        """Test salience with active patterns"""
        score = salience_scorer.compute_salience(
            'apl15',
            active_patterns={'apl12', 'apl13', 'apl14'}
        )
        assert 0 <= score <= 1
        assert score > 0
    
    def test_compute_salience_with_forces(self, salience_scorer):
        """Test salience with problem forces"""
        score = salience_scorer.compute_salience(
            'apl12',
            problem_forces=['community', 'social']
        )
        assert 0 <= score <= 1
        assert score > 0
    
    def test_compute_salience_all_factors(self, salience_scorer):
        """Test salience with all factors"""
        score = salience_scorer.compute_salience(
            'apl12',
            context_keywords=['community'],
            active_patterns={'apl13'},
            problem_forces=['social']
        )
        assert 0 <= score <= 1
        assert score > 0
    
    def test_compute_salience_custom_weights(self, salience_scorer):
        """Test salience with custom weights"""
        weights = {
            'centrality': 0.5,
            'relevance': 0.2,
            'gestalt': 0.2,
            'force': 0.1
        }
        score = salience_scorer.compute_salience(
            'apl12',
            weights=weights
        )
        assert 0 <= score <= 1
    
    def test_rank_patterns_basic(self, salience_scorer):
        """Test basic pattern ranking"""
        top = salience_scorer.rank_patterns(top_k=10)
        
        assert len(top) == 10
        assert all(isinstance(pid, str) for pid, _ in top)
        assert all(0 <= score <= 1 for _, score in top)
        
        # Check that results are sorted descending
        scores = [score for _, score in top]
        assert scores == sorted(scores, reverse=True)
    
    def test_rank_patterns_with_context(self, salience_scorer):
        """Test pattern ranking with context"""
        top = salience_scorer.rank_patterns(
            context_keywords=['community', 'housing'],
            top_k=5
        )
        
        assert len(top) == 5
        # Top patterns should have higher scores than baseline
        assert top[0][1] > 0
    
    def test_find_pattern_clusters(self, salience_scorer):
        """Test pattern cluster detection"""
        clusters = salience_scorer.find_pattern_clusters(min_size=3)
        
        assert len(clusters) > 0
        assert all(isinstance(c, set) for c in clusters)
        assert all(len(c) >= 3 for c in clusters)
        
        # Check that clusters contain valid pattern IDs
        for cluster in clusters:
            for pid in cluster:
                assert pid in salience_scorer.patterns


class TestCognitiveAffordances:
    """Test cognitive affordances for salience"""
    
    def test_centrality_identifies_important_patterns(self, salience_scorer):
        """Test that centrality identifies structurally important patterns"""
        centrality = salience_scorer.compute_centrality()
        
        # Get top central patterns
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top patterns should have non-zero centrality
        assert all(score > 0 for _, score in top_central)
        
        # Centrality should vary across patterns
        scores = [score for _, score in top_central]
        assert len(set(scores)) > 1  # Not all the same
    
    def test_context_guides_attention(self, salience_scorer):
        """Test that context keywords guide attention to relevant patterns"""
        context = ['community', 'neighborhood']
        
        # Rank with context
        with_context = salience_scorer.rank_patterns(
            context_keywords=context,
            top_k=5
        )
        
        # Rank without context (baseline)
        without_context = salience_scorer.rank_patterns(top_k=5)
        
        # Results should be different
        with_ids = [pid for pid, _ in with_context]
        without_ids = [pid for pid, _ in without_context]
        assert with_ids != without_ids
    
    def test_gestalt_emergence_detection(self, salience_scorer):
        """Test that gestalt scores identify emergent patterns"""
        active = {'apl12', 'apl13', 'apl14'}
        
        # Find patterns with high gestalt scores
        gestalt_scores = []
        for pid in list(salience_scorer.patterns.keys())[:50]:  # Sample
            if pid not in active:
                score = salience_scorer.compute_gestalt_score(pid, active)
                if score > 0:
                    gestalt_scores.append((pid, score))
        
        # Should find some patterns with gestalt scores
        assert len(gestalt_scores) > 0
        
        # Scores should vary
        scores = [score for _, score in gestalt_scores]
        if len(scores) > 1:
            assert len(set(scores)) > 1


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_nonexistent_pattern_salience(self, salience_scorer):
        """Test salience for non-existent pattern"""
        score = salience_scorer.compute_salience('apl999')
        assert score == 0
    
    def test_nonexistent_pattern_relevance(self, salience_scorer):
        """Test relevance for non-existent pattern"""
        score = salience_scorer.compute_context_relevance('apl999', ['test'])
        assert score == 0
    
    def test_nonexistent_pattern_gestalt(self, salience_scorer):
        """Test gestalt for non-existent pattern"""
        score = salience_scorer.compute_gestalt_score('apl999', {'apl1'})
        assert score == 0
    
    def test_empty_inputs(self, salience_scorer):
        """Test with empty inputs"""
        # Empty context
        top = salience_scorer.rank_patterns(context_keywords=[], top_k=5)
        assert len(top) == 5
        
        # Empty active patterns
        top = salience_scorer.rank_patterns(active_patterns=set(), top_k=5)
        assert len(top) == 5
        
        # Empty forces
        top = salience_scorer.rank_patterns(problem_forces=[], top_k=5)
        assert len(top) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
