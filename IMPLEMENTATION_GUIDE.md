# Pattern Language Implementation Guide

## Overview

This guide provides concrete implementation strategies for the paradigm and language recommendations in `PARADIGM_LANGUAGE_ANALYSIS.md`. It focuses on achieving cognitive "optimal grip" on the gestalt salience landscape through practical code examples and architectural patterns.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Datalog Query Layer](#datalog-query-layer)
3. [Haskell Transformation Engine](#haskell-transformation-engine)
4. [Python Salience System](#python-salience-system)
5. [Visualization Framework](#visualization-framework)
6. [Integration Architecture](#integration-architecture)
7. [Example Workflows](#example-workflows)

## Quick Start

### Current Implementation Status

✅ **Already Implemented:**
- OpenCog Atomese hypergraph representation
- Python schema generation and validation
- JSON data structures
- Basic testing infrastructure

🔨 **To Implement:**
- Datalog query layer
- Haskell transformation engine
- Salience scoring system
- Interactive visualization

### Prerequisites

```bash
# Already in repository
python3 -m pip install networkx jsonschema

# New dependencies
pip install datascript pyDatalog  # Datalog
npm install d3 d3-force-3d         # Visualization
```

## Datalog Query Layer

### Implementation Strategy

Use **pyDatalog** for Python integration or **Datomic** for production systems.

### Setup

```python
# datalog_queries.py
from pyDatalog import pyDatalog

# Initialize pyDatalog
pyDatalog.create_terms('Pattern, Category, Sequence, InCategory, InSequence, DependsOn')
pyDatalog.create_terms('X, Y, Z, P, C, S')

def load_patterns_from_atomese(atomese_file):
    """Load OpenCog Atomese into Datalog facts"""
    # Parse Atomese and convert to Datalog facts
    # (InheritanceLink Pattern-42 Category-Towns) -> +InCategory('Pattern-42', 'Category-Towns')
    pass

def define_rules():
    """Define Datalog rules for pattern inference"""
    
    # Transitive dependencies
    (DependsOn(X, Y) <= (DependsOn(X, Z) & DependsOn(Z, Y)))
    
    # Patterns in same category
    InSameCategory = pyDatalog.create_terms('InSameCategory')
    (InSameCategory(X, Y) <= (InCategory(X, C) & InCategory(Y, C) & (X != Y)))
    
    # Find pattern sequences
    SequencePath = pyDatalog.create_terms('SequencePath')
    (SequencePath(X, Y) <= (InSequence(X, S) & InSequence(Y, S) & DependsOn(X, Y)))
```

### Query Examples

```python
# Query 1: Find all patterns in Towns category
def find_patterns_in_category(category_name):
    """Find all patterns belonging to a category"""
    results = InCategory(X, category_name)
    return [str(pattern) for pattern in results]

# Query 2: Find transitive dependencies
def find_all_dependencies(pattern_id):
    """Find all patterns that depend on this pattern (transitively)"""
    results = DependsOn(X, pattern_id)
    return [str(p) for p in results]

# Query 3: Find related patterns (same category, connected by sequence)
def find_related_patterns(pattern_id):
    """Find patterns related through category or sequence membership"""
    # Patterns in same category
    same_cat = InSameCategory(pattern_id, X)
    # Patterns in connecting sequences
    in_seq = SequencePath(pattern_id, Y)
    
    return {
        'same_category': [str(p) for p in same_cat],
        'in_sequence': [str(p) for p in in_seq]
    }

# Query 4: Find optimal pattern sequence for a goal
def find_pattern_path(start_pattern, end_pattern):
    """Find path through pattern dependencies"""
    # Use recursive query to find path
    Path = pyDatalog.create_terms('Path')
    (Path(X, Y) <= DependsOn(X, Y))
    (Path(X, Z) <= (DependsOn(X, Y) & Path(Y, Z)))
    
    results = Path(start_pattern, end_pattern)
    return reconstruct_path(results)
```

### Integration with OpenCog Atomese

```python
# atomese_to_datalog.py
import re

def convert_atomese_to_datalog(scm_file):
    """Convert OpenCog Atomese .scm to Datalog facts"""
    
    with open(scm_file, 'r') as f:
        content = f.read()
    
    facts = []
    
    # Parse InheritanceLink -> InCategory fact
    inheritance_pattern = r'\(InheritanceLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
    for match in re.finditer(inheritance_pattern, content):
        pattern_id, category = match.groups()
        facts.append(f"+InCategory('{pattern_id}', '{category}')")
    
    # Parse MemberLink -> InSequence fact
    member_pattern = r'\(MemberLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
    for match in re.finditer(member_pattern, content):
        pattern_id, sequence = match.groups()
        facts.append(f"+InSequence('{pattern_id}', '{sequence}')")
    
    # Parse ImplicationLink -> DependsOn fact
    implication_pattern = r'\(ImplicationLink\s+\(ConceptNode "([^"]+)"\)\s+\(ConceptNode "([^"]+)"\)\)'
    for match in re.finditer(implication_pattern, content):
        from_pattern, to_pattern = match.groups()
        facts.append(f"+DependsOn('{from_pattern}', '{to_pattern}')")
    
    return facts

# Load facts
facts = convert_atomese_to_datalog('opencog_atomese/pattern_language.scm')
for fact in facts:
    exec(fact)  # Add facts to Datalog knowledge base
```

## Haskell Transformation Engine

### Domain Transformation System

```haskell
-- PatternTransform.hs
{-# LANGUAGE OverloadedStrings #-}

module PatternTransform where

import Data.Text (Text, replace)
import Data.Map (Map)
import qualified Data.Map as Map

-- Domain types
data Domain = Physical | Social | Conceptual | Psychic
  deriving (Show, Eq, Ord)

-- Placeholder with domain-specific mappings
data Placeholder = Placeholder
  { placeholderName :: Text
  , mappings :: Map Domain Text
  } deriving (Show, Eq)

-- Archetypal pattern with placeholders
data ArchetypalPattern = ArchetypalPattern
  { patternId :: Text
  , patternName :: Text
  , template :: Text
  , placeholders :: [Placeholder]
  } deriving (Show, Eq)

-- Transform archetypal pattern to specific domain
transform :: ArchetypalPattern -> Domain -> Text
transform pattern domain =
  foldl (substitutePlaceholder domain) (template pattern) (placeholders pattern)

-- Substitute a single placeholder
substitutePlaceholder :: Domain -> Text -> Placeholder -> Text
substitutePlaceholder domain text placeholder =
  case Map.lookup domain (mappings placeholder) of
    Just replacement -> replace key replacement text
    Nothing -> text
  where
    key = "{{" <> placeholderName placeholder <> "}}"

-- Transform to all domains
transformAll :: ArchetypalPattern -> Map Domain Text
transformAll pattern =
  Map.fromList [(domain, transform pattern domain) | domain <- allDomains]
  where
    allDomains = [Physical, Social, Conceptual, Psychic]

-- Example: Create a pattern
examplePattern :: ArchetypalPattern
examplePattern = ArchetypalPattern
  { patternId = "12610010"
  , patternName = "Independent domains"
  , template = "Balance between {{domains}} will not be achieved unless each one is small and autonomous."
  , placeholders = [domainsPlaceholder]
  }
  where
    domainsPlaceholder = Placeholder
      { placeholderName = "domains"
      , mappings = Map.fromList
          [ (Physical, "regions")
          , (Social, "functional domains")
          , (Conceptual, "knowledge domains")
          , (Psychic, "modes of awareness")
          ]
      }

-- Pattern composition: Combine multiple patterns
compose :: [ArchetypalPattern] -> Domain -> [Text]
compose patterns domain = map (\p -> transform p domain) patterns

-- Validate pattern transformation
validateTransform :: ArchetypalPattern -> Domain -> Either Text Text
validateTransform pattern domain =
  case hasMissingMappings pattern domain of
    [] -> Right (transform pattern domain)
    missing -> Left ("Missing mappings for: " <> show missing)

hasMissingMappings :: ArchetypalPattern -> Domain -> [Text]
hasMissingMappings pattern domain =
  [placeholderName ph | ph <- placeholders pattern, 
                        not (Map.member domain (mappings ph))]
```

### Type-Safe Pattern Sequences

```haskell
-- PatternSequence.hs
module PatternSequence where

import PatternTransform

-- Pattern sequence with ordering
data PatternSequence = PatternSequence
  { sequenceId :: Text
  , sequenceName :: Text
  , patterns :: [ArchetypalPattern]
  , emergentPhenomena :: Text
  } deriving (Show, Eq)

-- Transform entire sequence to domain
transformSequence :: PatternSequence -> Domain -> [Text]
transformSequence seq domain = map (\p -> transform p domain) (patterns seq)

-- Verify sequence integrity (all patterns have required domain mappings)
verifySequence :: PatternSequence -> Domain -> Either Text PatternSequence
verifySequence seq domain =
  case concatMap (\p -> hasMissingMappings p domain) (patterns seq) of
    [] -> Right seq
    missing -> Left ("Sequence has missing mappings: " <> show missing)

-- Extract pattern forces (for constraint solving)
type Force = (Text, Double)  -- (force_name, strength)

extractForces :: ArchetypalPattern -> [Force]
extractForces pattern = 
  -- Parse pattern text to extract forces
  -- This would analyze the pattern content for force indicators
  []  -- Placeholder implementation
```

### JSON Integration

```haskell
-- JSONBridge.hs
{-# LANGUAGE DeriveGeneric #-}

module JSONBridge where

import Data.Aeson
import GHC.Generics
import PatternTransform
import qualified Data.ByteString.Lazy as B

-- JSON-compatible types
data JSONPattern = JSONPattern
  { json_pattern_id :: Text
  , json_name :: Text
  , json_archetypal_pattern :: Text
  , json_placeholders :: [Text]
  , json_domain_mappings :: Map Text (Map Text Text)
  } deriving (Generic, Show)

instance FromJSON JSONPattern where
  parseJSON = withObject "JSONPattern" $ \v -> JSONPattern
    <$> v .: "pattern_id"
    <*> v .: "name"
    <*> v .: "archetypal_pattern"
    <*> v .: "placeholders"
    <*> v .: "domain_mappings"

instance ToJSON JSONPattern

-- Convert JSON to Haskell pattern
fromJSON :: JSONPattern -> ArchetypalPattern
fromJSON jp = ArchetypalPattern
  { patternId = json_pattern_id jp
  , patternName = json_name jp
  , template = json_archetypal_pattern jp
  , placeholders = createPlaceholders jp
  }
  where
    createPlaceholders jp =
      [Placeholder name (parseDomainMap mappings)
        | name <- json_placeholders jp
        , let mappings = Map.lookup name (json_domain_mappings jp)
      ]
    parseDomainMap Nothing = Map.empty
    parseDomainMap (Just m) = Map.mapKeys parseDomain m
    parseDomain "physical" = Physical
    parseDomain "social" = Social
    parseDomain "conceptual" = Conceptual
    parseDomain "psychic" = Psychic

-- Load patterns from JSON file
loadPatternsFromJSON :: FilePath -> IO [ArchetypalPattern]
loadPatternsFromJSON path = do
  content <- B.readFile path
  case decode content of
    Just patterns -> return (map fromJSON patterns)
    Nothing -> error "Failed to parse JSON"
```

## Python Salience System

### Salience Computation Framework

```python
# salience_engine.py
import numpy as np
from typing import List, Dict, Set
import networkx as nx

class SalienceEngine:
    """Compute pattern salience in context for optimal grip"""
    
    def __init__(self, pattern_graph: nx.MultiDiGraph):
        self.graph = pattern_graph
        self.centrality = nx.pagerank(pattern_graph)
        
    def compute_salience(self, pattern_id: str, context: Dict) -> float:
        """
        Compute pattern salience given context
        
        Salience = weighted combination of:
        - Relevance (semantic similarity to context)
        - Centrality (position in pattern network)
        - Emergence (gestalt formation potential)
        - Applicability (can pattern be applied in context)
        """
        relevance = self._compute_relevance(pattern_id, context)
        centrality = self.centrality.get(pattern_id, 0.0)
        emergence = self._compute_emergence(pattern_id, context)
        applicability = self._compute_applicability(pattern_id, context)
        
        # Weighted combination
        salience = (
            0.4 * relevance +
            0.2 * centrality +
            0.3 * emergence +
            0.1 * applicability
        )
        
        return salience
    
    def _compute_relevance(self, pattern_id: str, context: Dict) -> float:
        """Semantic similarity between pattern and context"""
        pattern = self.graph.nodes[pattern_id]
        
        # Simple keyword matching (replace with embeddings for production)
        pattern_text = pattern.get('problem', '') + ' ' + pattern.get('solution', '')
        context_text = ' '.join(str(v) for v in context.values())
        
        pattern_words = set(pattern_text.lower().split())
        context_words = set(context_text.lower().split())
        
        if not pattern_words or not context_words:
            return 0.0
        
        intersection = pattern_words & context_words
        union = pattern_words | context_words
        
        return len(intersection) / len(union)  # Jaccard similarity
    
    def _compute_emergence(self, pattern_id: str, context: Dict) -> float:
        """Potential for gestalt formation with active patterns"""
        active_patterns = context.get('active_patterns', set())
        
        if not active_patterns:
            return 0.0
        
        # Count connections to active patterns
        connections = 0
        for active_id in active_patterns:
            if self.graph.has_edge(pattern_id, active_id) or \
               self.graph.has_edge(active_id, pattern_id):
                connections += 1
        
        # Normalize by max possible connections
        max_connections = len(active_patterns)
        return connections / max_connections if max_connections > 0 else 0.0
    
    def _compute_applicability(self, pattern_id: str, context: Dict) -> float:
        """Can pattern be applied in current context?"""
        pattern = self.graph.nodes[pattern_id]
        
        # Check if context satisfies pattern prerequisites
        prerequisites = pattern.get('prerequisites', [])
        satisfied_prereqs = sum(
            1 for prereq in prerequisites 
            if prereq in context.get('satisfied_patterns', set())
        )
        
        if not prerequisites:
            return 1.0
        
        return satisfied_prereqs / len(prerequisites)
    
    def rank_patterns_by_salience(self, context: Dict, top_k: int = 10) -> List[tuple]:
        """Return top-k most salient patterns for context"""
        saliences = [
            (pattern_id, self.compute_salience(pattern_id, context))
            for pattern_id in self.graph.nodes()
        ]
        
        saliences.sort(key=lambda x: x[1], reverse=True)
        return saliences[:top_k]
    
    def compute_salience_landscape(self, context: Dict) -> Dict[str, float]:
        """Compute salience for all patterns (for visualization)"""
        return {
            pattern_id: self.compute_salience(pattern_id, context)
            for pattern_id in self.graph.nodes()
        }

# Usage example
def example_usage():
    # Load pattern graph
    import json
    with open('pattern_language_generated.json') as f:
        data = json.load(f)
    
    # Build graph
    G = nx.MultiDiGraph()
    for pattern in data['patterns']:
        G.add_node(pattern['id'], **pattern)
    
    # Create salience engine
    engine = SalienceEngine(G)
    
    # Define context
    context = {
        'domain': 'urban_planning',
        'scale': 'neighborhood',
        'active_patterns': {'Pattern-7', 'Pattern-28'},
        'satisfied_patterns': {'Pattern-1', 'Pattern-2'},
        'keywords': ['community', 'public space', 'gathering']
    }
    
    # Compute salient patterns
    salient = engine.rank_patterns_by_salience(context, top_k=5)
    for pattern_id, salience in salient:
        print(f"{pattern_id}: {salience:.3f}")
```

### Gestalt Detection

```python
# gestalt_detector.py
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class GestaltDetector:
    """Detect emergent gestalts from pattern combinations"""
    
    def __init__(self, pattern_graph: nx.MultiDiGraph):
        self.graph = pattern_graph
        
    def detect_gestalts(self, active_patterns: Set[str]) -> List[Set[str]]:
        """
        Detect gestalt groups in active patterns
        
        A gestalt is a group of patterns that:
        1. Are densely connected
        2. Have complementary forces
        3. Form a coherent whole
        """
        if len(active_patterns) < 2:
            return []
        
        # Create subgraph of active patterns
        subgraph = self.graph.subgraph(active_patterns)
        
        # Method 1: Community detection
        from networkx.algorithms import community
        communities = community.greedy_modularity_communities(subgraph.to_undirected())
        
        # Method 2: Force analysis
        force_gestalts = self._detect_by_forces(active_patterns)
        
        # Combine results
        all_gestalts = [set(c) for c in communities] + force_gestalts
        
        # Filter small gestalts
        return [g for g in all_gestalts if len(g) >= 2]
    
    def _detect_by_forces(self, active_patterns: Set[str]) -> List[Set[str]]:
        """Detect gestalts by complementary forces"""
        # Extract pattern forces
        pattern_forces = {}
        for pattern_id in active_patterns:
            pattern = self.graph.nodes[pattern_id]
            forces = pattern.get('forces', [])
            pattern_forces[pattern_id] = set(forces)
        
        # Find patterns with complementary forces
        gestalts = []
        visited = set()
        
        for p1 in active_patterns:
            if p1 in visited:
                continue
            
            gestalt = {p1}
            forces1 = pattern_forces[p1]
            
            for p2 in active_patterns:
                if p2 == p1 or p2 in visited:
                    continue
                
                forces2 = pattern_forces[p2]
                
                # Check if forces complement each other
                if self._forces_complement(forces1, forces2):
                    gestalt.add(p2)
            
            if len(gestalt) >= 2:
                gestalts.append(gestalt)
                visited.update(gestalt)
        
        return gestalts
    
    def _forces_complement(self, forces1: Set, forces2: Set) -> bool:
        """Check if two force sets complement each other"""
        # Simplified: forces complement if they share some but not all
        intersection = forces1 & forces2
        return 0 < len(intersection) < min(len(forces1), len(forces2))
    
    def compute_gestalt_strength(self, gestalt: Set[str]) -> float:
        """Compute strength of a gestalt (how well it holds together)"""
        if len(gestalt) < 2:
            return 0.0
        
        # Measure internal connectivity
        subgraph = self.graph.subgraph(gestalt)
        density = nx.density(subgraph)
        
        # Measure force balance
        all_forces = []
        for pattern_id in gestalt:
            pattern = self.graph.nodes[pattern_id]
            all_forces.extend(pattern.get('forces', []))
        
        # Force diversity (more diverse = stronger gestalt)
        force_diversity = len(set(all_forces)) / len(all_forces) if all_forces else 0
        
        return 0.6 * density + 0.4 * force_diversity
```

## Visualization Framework

### D3.js Interactive Pattern Graph

```javascript
// pattern_viz.js
class PatternGraphViz {
  constructor(containerId) {
    this.container = d3.select(`#${containerId}`);
    this.width = this.container.node().getBoundingClientRect().width;
    this.height = this.container.node().getBoundingClientRect().height;
    
    this.svg = this.container.append('svg')
      .attr('width', this.width)
      .attr('height', this.height);
    
    this.simulation = null;
    this.patterns = [];
    this.links = [];
  }
  
  loadData(patterns, relationships) {
    this.patterns = patterns.map(p => ({
      id: p.pattern_id,
      name: p.name,
      salience: p.salience || 0,
      category: p.category,
      radius: 5 + p.salience * 10
    }));
    
    this.links = relationships.map(r => ({
      source: r.from,
      target: r.to,
      type: r.relationship_type
    }));
    
    this.render();
  }
  
  render() {
    // Clear previous render
    this.svg.selectAll('*').remove();
    
    // Create force simulation
    this.simulation = d3.forceSimulation(this.patterns)
      .force('link', d3.forceLink(this.links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(d => d.radius + 5))
      .force('salience', this.salienceForce());
    
    // Draw links
    const link = this.svg.append('g')
      .selectAll('line')
      .data(this.links)
      .enter().append('line')
      .attr('stroke', d => this.linkColor(d.type))
      .attr('stroke-width', 1.5)
      .attr('stroke-opacity', 0.6);
    
    // Draw nodes
    const node = this.svg.append('g')
      .selectAll('circle')
      .data(this.patterns)
      .enter().append('circle')
      .attr('r', d => d.radius)
      .attr('fill', d => this.nodeColor(d))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .call(this.drag());
    
    // Add labels
    const label = this.svg.append('g')
      .selectAll('text')
      .data(this.patterns)
      .enter().append('text')
      .text(d => d.name)
      .attr('font-size', 10)
      .attr('dx', d => d.radius + 5)
      .attr('dy', 4);
    
    // Add tooltips
    node.append('title')
      .text(d => `${d.name}\nSalience: ${d.salience.toFixed(3)}`);
    
    // Update positions on tick
    this.simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      
      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      
      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });
  }
  
  salienceForce() {
    // Custom force: pull high-salience patterns toward top
    return alpha => {
      this.patterns.forEach(p => {
        const targetY = this.height * (1 - p.salience);
        p.vy += (targetY - p.y) * alpha * 0.1;
      });
    };
  }
  
  nodeColor(pattern) {
    // Color by salience (blue = low, red = high)
    const hue = (1 - pattern.salience) * 240;  // 240=blue, 0=red
    return d3.hsl(hue, 0.7, 0.5);
  }
  
  linkColor(type) {
    const colors = {
      'depends_on': '#999',
      'category': '#6c6',
      'sequence': '#66c',
      'conflict': '#c66'
    };
    return colors[type] || '#999';
  }
  
  drag() {
    function dragstarted(event, d) {
      if (!event.active) this.simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event, d) {
      if (!event.active) this.simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    
    return d3.drag()
      .on('start', dragstarted.bind(this))
      .on('drag', dragged.bind(this))
      .on('end', dragended.bind(this));
  }
  
  highlightGestalts(gestalts) {
    // Highlight patterns that form gestalts
    this.svg.selectAll('circle')
      .attr('stroke', d => {
        const inGestalt = gestalts.some(g => g.has(d.id));
        return inGestalt ? '#ff0' : '#fff';
      })
      .attr('stroke-width', d => {
        const inGestalt = gestalts.some(g => g.has(d.id));
        return inGestalt ? 4 : 2;
      });
  }
}

// Usage
const viz = new PatternGraphViz('pattern-graph-container');

// Load data from API
fetch('/api/patterns/with-salience?context=' + JSON.stringify(context))
  .then(r => r.json())
  .then(data => {
    viz.loadData(data.patterns, data.relationships);
    viz.highlightGestalts(data.gestalts);
  });
```

### Salience Landscape Heatmap

```javascript
// salience_landscape.js
class SalienceLandscape {
  constructor(containerId) {
    this.container = d3.select(`#${containerId}`);
    this.width = this.container.node().getBoundingClientRect().width;
    this.height = this.container.node().getBoundingClientRect().height;
    
    this.svg = this.container.append('svg')
      .attr('width', this.width)
      .attr('height', this.height);
  }
  
  render(patterns) {
    // Use MDS (multidimensional scaling) to position patterns in 2D
    const positions = this.computePositions(patterns);
    
    // Create contour plot of salience
    const contours = d3.contourDensity()
      .x(d => d.x)
      .y(d => d.y)
      .weight(d => d.salience)
      .size([this.width, this.height])
      .bandwidth(30)
      (positions);
    
    // Color scale
    const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
      .domain([0, d3.max(contours, d => d.value)]);
    
    // Draw contours
    this.svg.append('g')
      .selectAll('path')
      .data(contours)
      .enter().append('path')
      .attr('d', d3.geoPath())
      .attr('fill', d => colorScale(d.value))
      .attr('opacity', 0.5);
    
    // Draw pattern points
    this.svg.append('g')
      .selectAll('circle')
      .data(positions)
      .enter().append('circle')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', 4)
      .attr('fill', '#000')
      .append('title')
      .text(d => `${d.name}: ${d.salience.toFixed(3)}`);
  }
  
  computePositions(patterns) {
    // Use t-SNE or MDS to project patterns into 2D
    // For now, use simple force layout
    const simulation = d3.forceSimulation(patterns)
      .force('charge', d3.forceManyBody().strength(-50))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(10))
      .stop();
    
    // Run simulation
    for (let i = 0; i < 300; i++) simulation.tick();
    
    return patterns.map(p => ({
      x: p.x,
      y: p.y,
      name: p.name,
      salience: p.salience
    }));
  }
}
```

## Integration Architecture

### REST API with FastAPI

```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json

app = FastAPI(title="Pattern Language API")

# Initialize components
from salience_engine import SalienceEngine
from gestalt_detector import GestaltDetector
import networkx as nx

# Load pattern graph
with open('pattern_language_generated.json') as f:
    data = json.load(f)

G = nx.MultiDiGraph()
for pattern in data['patterns']:
    G.add_node(pattern['id'], **pattern)

salience_engine = SalienceEngine(G)
gestalt_detector = GestaltDetector(G)

# Models
class Context(BaseModel):
    domain: Optional[str] = None
    scale: Optional[str] = None
    active_patterns: List[str] = []
    satisfied_patterns: List[str] = []
    keywords: List[str] = []

class PatternResponse(BaseModel):
    pattern_id: str
    name: str
    salience: float
    category: str

# Endpoints
@app.get("/api/patterns")
async def get_all_patterns():
    """Get all patterns"""
    return {"patterns": list(G.nodes(data=True))}

@app.post("/api/patterns/salient")
async def get_salient_patterns(context: Context, top_k: int = 10):
    """Get most salient patterns for context"""
    context_dict = context.dict()
    context_dict['active_patterns'] = set(context_dict['active_patterns'])
    context_dict['satisfied_patterns'] = set(context_dict['satisfied_patterns'])
    
    salient = salience_engine.rank_patterns_by_salience(context_dict, top_k)
    
    return {
        "patterns": [
            {
                "pattern_id": pid,
                "name": G.nodes[pid].get('name', ''),
                "salience": sal,
                "category": G.nodes[pid].get('category', '')
            }
            for pid, sal in salient
        ]
    }

@app.post("/api/gestalts")
async def detect_gestalts(active_patterns: List[str]):
    """Detect gestalts in active patterns"""
    gestalts = gestalt_detector.detect_gestalts(set(active_patterns))
    
    return {
        "gestalts": [
            {
                "patterns": list(g),
                "strength": gestalt_detector.compute_gestalt_strength(g)
            }
            for g in gestalts
        ]
    }

@app.post("/api/patterns/transform")
async def transform_pattern(pattern_id: str, domain: str):
    """Transform archetypal pattern to specific domain"""
    # Call Haskell transformation service or use Python implementation
    # This would integrate with the Haskell transformation engine
    pass

@app.get("/api/patterns/landscape")
async def get_salience_landscape(context: Context):
    """Get full salience landscape for visualization"""
    context_dict = context.dict()
    landscape = salience_engine.compute_salience_landscape(context_dict)
    
    return {
        "landscape": landscape,
        "patterns": [
            {
                "pattern_id": pid,
                "name": G.nodes[pid].get('name', ''),
                "salience": landscape[pid]
            }
            for pid in G.nodes()
        ]
    }

# Run with: uvicorn api:app --reload
```

## Example Workflows

### Workflow 1: Find Relevant Patterns for Urban Design

```python
# urban_design_workflow.py

# 1. Define context
context = {
    'domain': 'urban_planning',
    'scale': 'neighborhood',
    'active_patterns': set(),
    'satisfied_patterns': set(),
    'keywords': ['community', 'gathering', 'public space']
}

# 2. Get salient patterns
salient_patterns = salience_engine.rank_patterns_by_salience(context, top_k=10)

print("Most relevant patterns:")
for pid, salience in salient_patterns:
    pattern = G.nodes[pid]
    print(f"  {pid}: {pattern['name']} (salience: {salience:.3f})")

# 3. Select patterns to apply
selected = [pid for pid, _ in salient_patterns[:5]]
context['active_patterns'] = set(selected)

# 4. Detect emerging gestalts
gestalts = gestalt_detector.detect_gestalts(context['active_patterns'])

print("\nEmerging gestalts:")
for i, gestalt in enumerate(gestalts):
    strength = gestalt_detector.compute_gestalt_strength(gestalt)
    print(f"  Gestalt {i+1} (strength: {strength:.3f}):")
    for pid in gestalt:
        print(f"    - {G.nodes[pid]['name']}")

# 5. Transform to specific domain
if archetypal_patterns:
    for pid in selected:
        if is_archetypal(pid):
            physical_version = transform_to_domain(pid, 'physical')
            print(f"\n{pid} (Physical): {physical_version}")
```

### Workflow 2: Pattern Sequence Discovery

```python
# sequence_discovery.py

# 1. Start with a goal pattern
goal_pattern = "Pattern-42"  # Community of 7000

# 2. Find prerequisites using Datalog
prerequisites = find_all_dependencies(goal_pattern)

print(f"Patterns needed before {goal_pattern}:")
for prereq in prerequisites:
    print(f"  - {prereq}")

# 3. Find optimal sequence using constraint solving
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Create variables for pattern ordering
pattern_vars = {p: model.NewIntVar(0, 100, f'order_{p}') 
                for p in prerequisites + [goal_pattern]}

# Add dependency constraints
for p1, p2 in dependency_pairs:
    model.Add(pattern_vars[p1] < pattern_vars[p2])

# Add spatial constraints (if applicable)
# model.Add(adjacent(p1, p2) -> |position[p1] - position[p2]| < threshold)

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    sequence = sorted(pattern_vars.items(), key=lambda x: solver.Value(x[1]))
    print("\nOptimal pattern sequence:")
    for pattern, _ in sequence:
        print(f"  {pattern}: {G.nodes[pattern]['name']}")
```

## Next Steps

1. **Implement Datalog Layer**
   - Set up pyDatalog or Datomic
   - Convert Atomese to Datalog facts
   - Create query library

2. **Build Haskell Transformation Service**
   - Implement pattern transformation library
   - Create REST API wrapper
   - Integrate with Python API

3. **Deploy Salience System**
   - Implement salience engine
   - Train ML models for relevance
   - Add gestalt detection

4. **Create Visualization**
   - Build D3.js interactive graph
   - Implement salience landscape viewer
   - Add gestalt highlighting

5. **Integration Testing**
   - Test end-to-end workflows
   - Validate cognitive affordances
   - Measure performance

## References

- OpenCog Atomese Documentation
- pyDatalog User Guide
- Haskell Aeson for JSON
- D3.js Force Layout Examples
- FastAPI Documentation
