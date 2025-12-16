# Quick Reference: Pattern Language Implementation Stack

## TL;DR - Recommended Stack

```
Foundation:  Scheme/OpenCog (✅ implemented)
Queries:     Datalog/pyDatalog (📋 recommended)
Transforms:  Haskell (📋 recommended)
Integration: Python + FastAPI (🔶 partial)
Viz:         JavaScript + D3.js (📋 recommended)
```

## Getting Started

### 1. Use Current Implementation (Hypergraph)

```bash
# Load OpenCog Atomese representation
python3 demo_opencog_atomese.py

# View enhanced features
python3 demo_enhanced_atomese.py
```

### 2. Try Datalog Queries (Demo)

```bash
# Install pyDatalog
pip install pyDatalog

# Run query demo
python3 demo_datalog_queries.py
```

### 3. Read Analysis

```bash
# Quick overview
cat OPTIMAL_GRIP_ANALYSIS.md

# Detailed analysis
cat PARADIGM_LANGUAGE_ANALYSIS.md

# Code examples
cat IMPLEMENTATION_GUIDE.md

# Comparison matrices
cat PARADIGM_COMPARISON_MATRIX.md
```

## When to Use Each Paradigm/Language

### Use Hypergraph (Scheme/OpenCog) When:
- ✅ Storing pattern relationships
- ✅ Multi-way connections
- ✅ Category hierarchies
- ✅ Pattern sequences
- **Status**: ✅ Already implemented

### Use Logic (Datalog) When:
- 📋 Querying patterns declaratively
- 📋 Finding transitive relationships
- 📋 Pattern discovery
- 📋 Inference
- **Status**: 🔶 Demo available

### Use Functional (Haskell) When:
- 📋 Domain transformations (physical→social→conceptual→psychic)
- 📋 Type-safe pattern composition
- 📋 Placeholder substitution
- 📋 Validation
- **Status**: 📋 Examples provided

### Use Python When:
- 🔶 System integration
- 📋 ML-based salience scoring
- 📋 Constraint solving
- 📋 REST APIs
- **Status**: 🔶 Partial (schema generation only)

### Use JavaScript/D3 When:
- 📋 Interactive visualization
- 📋 Web interfaces
- 📋 Gestalt highlighting
- 📋 Salience landscape
- **Status**: 📋 Examples provided

## Code Examples

### Example 1: Query Patterns (Datalog)

```python
from demo_datalog_queries import PatternLanguageQuerySystem

# Initialize
system = PatternLanguageQuerySystem('pattern_language_generated.json')

# Find patterns in category
patterns = system.find_patterns_in_category('Category-Towns')

# Find dependencies
deps = system.find_all_dependencies('Pattern-42')

# Find related patterns
related = system.find_related_patterns('Pattern-42')

# Context-based search
results = system.find_patterns_by_context(
    keywords=['community', 'public'],
    active_patterns={'Pattern-7'}
)
```

### Example 2: Transform Patterns (Haskell)

```haskell
import PatternTransform

-- Load archetypal pattern
let pattern = ArchetypalPattern
      { patternId = "12610010"
      , template = "Balance between {{domains}} will not be achieved..."
      , placeholders = [domainsPlaceholder]
      }

-- Transform to physical domain
let physical = transform pattern Physical
-- Result: "Balance between regions will not be achieved..."

-- Transform to all domains
let allDomains = transformAll pattern
```

### Example 3: Compute Salience (Python)

```python
from salience_engine import SalienceEngine
import networkx as nx

# Build graph from patterns
G = build_pattern_graph()

# Create salience engine
engine = SalienceEngine(G)

# Define context
context = {
    'domain': 'urban_planning',
    'keywords': ['community', 'public space'],
    'active_patterns': {'Pattern-7', 'Pattern-28'}
}

# Get salient patterns
salient = engine.rank_patterns_by_salience(context, top_k=10)
```

### Example 4: Visualize (JavaScript/D3)

```javascript
// Create visualization
const viz = new PatternGraphViz('container-id');

// Load data
fetch('/api/patterns/with-salience')
  .then(r => r.json())
  .then(data => {
    viz.loadData(data.patterns, data.relationships);
    viz.highlightGestalts(data.gestalts);
  });
```

## Architecture Layers

```
┌─────────────────────────────────────┐
│  Layer 5: Visualization             │
│  JavaScript + D3.js                 │  ← User sees gestalts
│  Status: 📋 Recommended             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 4: Integration               │
│  Python + FastAPI                   │  ← API, ML, orchestration
│  Status: 🔶 Partial (expand)        │
└─────────────────────────────────────┘
        ↓           ↓           ↓
┌────────────┐ ┌───────────┐ ┌────────────┐
│ Layer 3a:  │ │ Layer 3b: │ │ Layer 3c:  │
│ Queries    │ │ Transform │ │ Salience   │
│ Datalog    │ │ Haskell   │ │ Python ML  │
│ 📋 Rec'd   │ │ 📋 Rec'd  │ │ 📋 Rec'd   │
└────────────┘ └───────────┘ └────────────┘
        ↓           ↓           ↓
┌─────────────────────────────────────┐
│  Layer 1-2: Foundation              │
│  Scheme/OpenCog Atomese             │  ← Hypergraph storage
│  Status: ✅ Implemented              │
└─────────────────────────────────────┘
```

## Paradigm Selection Matrix

| Need | Use This | Not This |
|------|----------|----------|
| Store patterns | Hypergraph | OOP classes |
| Query patterns | Datalog | SQL/LINQ |
| Transform domains | Haskell | Mutations |
| Optimize sequences | Constraints | Heuristics |
| Score salience | ML (Python) | Rules only |
| Visualize | D3.js | Text output |
| Integrate | Python | Shell scripts |

## Cognitive Affordance Checklist

- ✅ Multi-scale perception → Hypergraph hierarchy
- ✅ Relationship richness → Hypergraph + Datalog
- ✅ Domain transformation → Haskell functions
- ✅ Contextual relevance → Datalog + ML
- ✅ Emergence tracking → Graph analysis + ML
- ✅ Force resolution → Constraint solving
- ✅ Temporal sequencing → Datalog + Constraints
- ✅ Interactive navigation → D3.js
- ✅ Gestalt perception → Clustering + D3.js
- ✅ Salience gradients → ML + D3.js heatmap

## Implementation Priority

### Priority 1: Query Layer (Datalog)
**Why**: Enables natural pattern discovery
**Effort**: Medium
**Impact**: High
**Status**: Demo available ✅

### Priority 2: Salience System (Python ML)
**Why**: Makes relevant patterns stand out
**Effort**: Medium
**Impact**: High
**Status**: Examples provided

### Priority 3: Visualization (D3.js)
**Why**: Makes abstract patterns concrete
**Effort**: High (web development)
**Impact**: Very High
**Status**: Examples provided

### Priority 4: Transform Engine (Haskell)
**Why**: Type-safe domain transformations
**Effort**: Medium-High
**Impact**: Medium
**Status**: Examples provided

### Priority 5: REST API (Python FastAPI)
**Why**: Integrates all components
**Effort**: Medium
**Impact**: Medium
**Status**: Examples provided

## Common Pitfalls

### ❌ Don't: Use Single Paradigm
Problem: No single approach achieves optimal grip
Solution: Use multi-layer architecture

### ❌ Don't: Ignore Existing OpenCog
Problem: Reinventing the wheel
Solution: Build on existing hypergraph foundation

### ❌ Don't: Over-engineer Early
Problem: Analysis paralysis
Solution: Start with demos, iterate

### ❌ Don't: Skip Visualization
Problem: Cognitive benefits lost without visual feedback
Solution: Prioritize D3.js layer

### ❌ Don't: Manual Queries
Problem: Imperative code obscures pattern relationships
Solution: Use declarative Datalog queries

## Resources

### Documentation
- `OPTIMAL_GRIP_ANALYSIS.md` - Overview
- `PARADIGM_LANGUAGE_ANALYSIS.md` - Detailed analysis
- `IMPLEMENTATION_GUIDE.md` - Code examples
- `PARADIGM_COMPARISON_MATRIX.md` - Matrices

### Code
- `demo_datalog_queries.py` - Query system demo
- `demo_opencog_atomese.py` - Hypergraph demo
- `opencog_atomese/` - Atomese implementation

### Data
- `pattern_language_generated.json` - APL patterns
- `archetypal_patterns.json` - UIA patterns
- `opencog_atomese/pattern_language.scm` - Atomese

## FAQ

**Q: Why not just use Neo4j?**
A: Neo4j is good but lacks: logic programming, type-safe transformations, ML integration. Multi-tool approach better.

**Q: Why Haskell if Python works?**
A: Type safety for domain transformations. Haskell catches transformation errors at compile time.

**Q: Can I skip Datalog?**
A: You can, but queries become imperative. Datalog makes pattern relationships explicit.

**Q: What's the minimal viable stack?**
A: Python + OpenCog Atomese + NetworkX + Matplotlib. But full stack achieves optimal grip.

**Q: Is this overkill?**
A: For simple pattern lookup, yes. For cognitive "optimal grip" on gestalt salience landscape, no.

## Next Steps

1. **Explore demos**: Run existing demos to understand current state
2. **Read analysis**: Understand why multi-paradigm approach needed
3. **Try Datalog**: Install pyDatalog and run query demo
4. **Plan integration**: Decide which layers to implement first
5. **Prototype viz**: Create simple D3.js pattern graph
6. **Iterate**: Build incrementally, test cognitive affordances

## Getting Help

- **General questions**: See full documentation in analysis files
- **Code examples**: See IMPLEMENTATION_GUIDE.md
- **Architecture**: See OPTIMAL_GRIP_ANALYSIS.md
- **Comparisons**: See PARADIGM_COMPARISON_MATRIX.md
- **Theory**: See PARADIGM_LANGUAGE_ANALYSIS.md

## Status Legend

- ✅ Implemented and working
- 🔶 Partially implemented
- 📋 Recommended but not implemented
- ⚠️ Not recommended
- ❌ Not suitable
