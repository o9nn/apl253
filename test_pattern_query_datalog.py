#!/usr/bin/env python3
"""
Tests for Pattern Language Datalog Query System

Tests Phase 2 implementation: Query & Transformation
"""

import pytest
from pathlib import Path
from pattern_query_datalog import PatternQuerySystem


@pytest.fixture
def query_system():
    """Create and initialize query system"""
    system = PatternQuerySystem()
    json_path = Path("pattern_language_generated.json")
    
    if json_path.exists():
        system.load_from_json(str(json_path))
    else:
        pytest.skip("pattern_language_generated.json not found")
    
    return system


class TestPatternQuerySystem:
    """Test suite for PatternQuerySystem"""
    
    def test_system_initialization(self, query_system):
        """Test that system initializes correctly"""
        assert query_system is not None
        assert len(query_system.patterns) > 0
        assert len(query_system.categories) > 0
        assert len(query_system.sequences) > 0
    
    def test_load_patterns(self, query_system):
        """Test pattern loading"""
        assert len(query_system.patterns) == 253
        assert 'apl1' in query_system.patterns
        assert 'apl253' in query_system.patterns
    
    def test_load_categories(self, query_system):
        """Test category loading"""
        categories = query_system.query_all_categories()
        assert 'Towns' in categories
        assert 'Buildings' in categories
        assert 'Construction' in categories
        assert len(categories) == 3
    
    def test_load_sequences(self, query_system):
        """Test sequence loading"""
        sequences = query_system.query_all_sequences()
        assert len(sequences) == 36
        assert 'Sequence-1' in sequences
        assert 'Sequence-36' in sequences
    
    def test_query_patterns_in_category(self, query_system):
        """Test querying patterns by category"""
        towns = query_system.query_patterns_in_category('Towns')
        assert len(towns) == 94
        assert 'apl1' in towns
        assert 'apl94' in towns
    
    def test_query_patterns_in_sequence(self, query_system):
        """Test querying patterns in a sequence"""
        seq1_patterns = query_system.query_patterns_in_sequence('Sequence-1')
        assert len(seq1_patterns) > 0
        assert 'apl1' in seq1_patterns
    
    def test_query_sequences_containing(self, query_system):
        """Test finding sequences containing a pattern"""
        sequences = query_system.query_sequences_containing('apl1')
        assert len(sequences) > 0
        assert 'Sequence-1' in sequences
    
    def test_query_related_patterns(self, query_system):
        """Test finding related patterns"""
        related = query_system.query_related_patterns('apl1')
        assert len(related) > 0
        # Should include other patterns in Towns category or Sequence-1
        assert any(p != 'apl1' for p in related)
    
    def test_query_transitive_dependencies(self, query_system):
        """Test transitive dependency queries"""
        # Test that patterns with preceding patterns have dependencies
        deps = query_system.query_transitive_dependencies('apl2')
        # apl2 may have dependencies based on preceding_patterns
        assert isinstance(deps, list)
    
    def test_query_pattern_name(self, query_system):
        """Test querying pattern names"""
        name = query_system.query_pattern_name('apl1')
        assert name == 'INDEPENDENT REGIONS'
    
    def test_query_pattern_context(self, query_system):
        """Test getting full pattern context"""
        context = query_system.get_pattern_context('apl1')
        assert context['pattern_id'] == 'apl1'
        assert context['name'] == 'INDEPENDENT REGIONS'
        assert 'Towns' in context['category']
        assert len(context['sequences']) > 0
        assert isinstance(context['related'], list)
        assert isinstance(context['dependencies'], list)
    
    def test_find_pattern_path(self, query_system):
        """Test pattern path finding"""
        # Test that we can check for dependency paths
        # This depends on the data structure
        result = query_system.find_pattern_path('apl1', 'apl2')
        assert isinstance(result, bool)
    
    def test_category_boundaries(self, query_system):
        """Test that patterns are in correct category ranges"""
        towns = query_system.query_patterns_in_category('Towns')
        buildings = query_system.query_patterns_in_category('Buildings')
        construction = query_system.query_patterns_in_category('Construction')
        
        # Check ranges
        assert all(int(p[3:]) <= 94 for p in towns)  # Towns: 1-94
        assert all(95 <= int(p[3:]) <= 204 for p in buildings)  # Buildings: 95-204
        assert all(205 <= int(p[3:]) <= 253 for p in construction)  # Construction: 205-253
    
    def test_inference_rules(self, query_system):
        """Test that inference rules work"""
        # Test same_category inference
        towns = query_system.query_patterns_in_category('Towns')
        if len(towns) >= 2:
            # Check that patterns in same category are related
            related = query_system.query_related_patterns(towns[0])
            # Should have at least some related patterns from same category
            assert len(related) > 0


class TestCognitiveAffordances:
    """Test cognitive affordances provided by the system"""
    
    def test_multi_scale_perception(self, query_system):
        """Test multi-scale perception (categories, sequences, patterns)"""
        # Can navigate from category -> patterns
        categories = query_system.query_all_categories()
        assert len(categories) > 0
        
        # Can navigate from sequences -> patterns
        sequences = query_system.query_all_sequences()
        assert len(sequences) > 0
        
        # Can get individual pattern details
        context = query_system.get_pattern_context('apl1')
        assert context is not None
    
    def test_relationship_richness(self, query_system):
        """Test multiple types of relationships"""
        # Test different relationship queries
        context = query_system.get_pattern_context('apl1')
        
        # Should have category relationships
        assert len(context['category']) > 0
        
        # Should have sequence relationships
        assert len(context['sequences']) > 0
        
        # Should have related patterns (by category or sequence)
        assert isinstance(context['related'], list)
    
    def test_fluid_navigation(self, query_system):
        """Test fluid navigation through pattern space"""
        # Start with a category
        towns = query_system.query_patterns_in_category('Towns')
        assert len(towns) > 0
        
        # Navigate to a specific pattern
        pattern = towns[0]
        context = query_system.get_pattern_context(pattern)
        
        # Navigate to related patterns
        related = context['related']
        assert len(related) > 0
        
        # Navigate to sequences
        sequences = context['sequences']
        assert len(sequences) > 0


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_query(self, query_system):
        """Test querying non-existent category"""
        results = query_system.query_patterns_in_category('NonExistent')
        assert len(results) == 0
    
    def test_nonexistent_pattern(self, query_system):
        """Test querying non-existent pattern"""
        name = query_system.query_pattern_name('apl999')
        assert name is None
    
    def test_empty_dependencies(self, query_system):
        """Test pattern with no dependencies"""
        deps = query_system.query_transitive_dependencies('apl1')
        # apl1 might have no dependencies
        assert isinstance(deps, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
