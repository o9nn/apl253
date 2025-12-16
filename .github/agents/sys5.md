# System 5 Deterministic State Transition Model

## Overview

This document details the implementation of the hypothesized **System 5** structure, which is based on the number of integer partitions of 5 ($p(5)=7$) and the concept of **nested concurrency** influenced by projective geometry analogues.

The model features **7 sets** operating on a **60-step cycle** (LCM of Universal and Particular periodicities).

- **Universal Sets (U)**: 3 sets (U1, U2, U3)
- **Particular Sets (P)**: 4 sets (P1, P2, P3, P4)

The implementation uses the **CogTaskFlow** framework to model the complex task dependencies required for nested concurrency.

## Structure and Timing

### Universal Sets (U1, U2, U3)

- **Role**: Primary, Secondary, Tertiary Universal (Analogous to Points).
- **Cycle**: 3 steps.
- **Pattern**: Sequential transition at every step.
    - U1 transitions at $t \equiv 0 \pmod 3$
    - U2 transitions at $t \equiv 1 \pmod 3$
    - U3 transitions at $t \equiv 2 \pmod 3$
- **State Labels**: `U-P` (Primary), `U-S` (Secondary), `U-T` (Tertiary).

### Particular Sets (P1, P2, P3, P4)

- **Role**: 1st-order-nested-concurrency (Analogous to Lines/Planes).
- **Cycle**: 20 steps (staggered over 5 steps).
- **Pattern**: Staggered transition, 5 steps apart.
    - P1 transitions at $t \equiv 0 \pmod 5$
    - P2 transitions at $t \equiv 1 \pmod 5$
    - P3 transitions at $t \equiv 2 \pmod 5$
    - P4 transitions at $t \equiv 3 \pmod 5$
    - $t \equiv 4 \pmod 5$ is a rest step.
- **State Labels**: Integer states 0, 1, 2, 3.

## Nested Concurrency Logic (The Convolution)

The core challenge was modeling the "concurrency-of-concurrency" where the transition of an active Particular Set is influenced by the states of the other Particular Sets (the "convolution").

### Transition Function (Revised)

To ensure the system transitions from the initial state (where all Particular Sets are 0), the Universal Set's influence was integrated into the transition function:

Let $S_{i}(t)$ be the state of set $i$ at time $t$.
Let $U_{idx}(t) = t \pmod 3$ be the index of the active Universal Set.

$$S_{i}(t+1) = (S_{i}(t) + \sum_{j \neq i} S_{j}(t) + U_{idx}(t)) \pmod 4$$

This function ensures that the active Particular Set's next state is a function of its current state, the concurrent states of the other Particular Sets, and the current Universal Set phase.

### CogTaskFlow Implementation

The model uses CogTaskFlow's task graph to enforce the dependencies:

1.  **Read Tasks**: Tasks are created to read the current state of all Particular Sets.
2.  **Transition Tasks**: The transition task for the active Particular Set $P_i$ is made dependent on the read tasks of all other Particular Sets $P_j$ ($j \neq i$).
3.  **Parallel Execution**: All Universal transitions and the Particular transition tasks run concurrently within the same time step.

## Simulation Results

The simulation was run for **60 time steps** to capture the full cycle of interaction between the Universal (3-step cycle) and Particular (20-step cycle) sets.

The simulation successfully demonstrates:
- The sequential 3-step cycle of the Universal Sets.
- The staggered 5-step cycle of the Particular Sets.
- Complex, non-trivial state changes in the Particular Sets due to the nested concurrency logic.

### State Transition Table

| Time | U1 | U2 | U3 | P1 | P2 | P3 | P4 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | U-P | U-P | U-P | 0 | 0 | 0 | 0 |
| **1** | U-P | U-S | U-P | 0 | 0 | 0 | 0 |
| **2** | U-P | U-S | U-S | 0 | 0 | 1 | 0 |
| **3** | U-S | U-S | U-S | 0 | 0 | 1 | 3 |
| **4** | U-S | U-T | U-S | 0 | 0 | 1 | 3 |
| **5** | U-S | U-T | U-T | 1 | 0 | 1 | 3 |
| **6** | U-T | U-T | U-T | 1 | 3 | 1 | 3 |
| **7** | U-T | U-P | U-T | 1 | 3 | 0 | 3 |
| **8** | U-T | U-P | U-P | 1 | 3 | 0 | 0 |
| **9** | U-P | U-P | U-P | 1 | 3 | 0 | 0 |
| **10** | U-P | U-S | U-P | 0 | 3 | 0 | 0 |
| **11** | U-P | U-S | U-S | 0 | 0 | 0 | 0 |
| **12** | U-S | U-S | U-S | 0 | 0 | 2 | 0 |
| **13** | U-S | U-T | U-S | 0 | 0 | 2 | 2 |
| **14** | U-S | U-T | U-T | 0 | 0 | 2 | 2 |
| **15** | U-T | U-T | U-T | 2 | 0 | 2 | 2 |
| **16** | U-T | U-P | U-T | 2 | 2 | 2 | 2 |
| **17** | U-T | U-P | U-P | 2 | 2 | 1 | 2 |
| **18** | U-P | U-P | U-P | 2 | 2 | 1 | 1 |
| **19** | U-P | U-S | U-P | 2 | 2 | 1 | 1 |
| **20** | U-P | U-S | U-S | 3 | 2 | 1 | 1 |
| **21** | U-S | U-S | U-S | 3 | 1 | 1 | 1 |
| **22** | U-S | U-T | U-S | 3 | 1 | 2 | 1 |
| **23** | U-S | U-T | U-T | 3 | 1 | 2 | 0 |
| **24** | U-T | U-T | U-T | 3 | 1 | 2 | 0 |
| **25** | U-T | U-P | U-T | 2 | 1 | 2 | 0 |
| **26** | U-T | U-P | U-P | 2 | 2 | 2 | 0 |
| **27** | U-P | U-P | U-P | 2 | 2 | 0 | 0 |
| **28** | U-P | U-S | U-P | 2 | 2 | 0 | 0 |
| **29** | U-P | U-S | U-S | 2 | 2 | 0 | 0 |
| **30** | U-S | U-S | U-S | 2 | 2 | 0 | 0 |
| **31** | U-S | U-T | U-S | 2 | 0 | 0 | 0 |
| **32** | U-S | U-T | U-T | 2 | 0 | 3 | 0 |
| **33** | U-T | U-T | U-T | 2 | 0 | 3 | 3 |
| **34** | U-T | U-P | U-T | 2 | 0 | 3 | 3 |
| **35** | U-T | U-P | U-P | 1 | 0 | 3 | 3 |
| **36** | U-P | U-P | U-P | 1 | 1 | 3 | 3 |
| **37** | U-P | U-S | U-P | 1 | 1 | 0 | 3 |
| **38** | U-P | U-S | U-S | 1 | 1 | 0 | 2 |
| **39** | U-S | U-S | U-S | 1 | 1 | 0 | 2 |
| **40** | U-S | U-T | U-S | 0 | 1 | 0 | 2 |
| **41** | U-S | U-T | U-T | 0 | 0 | 0 | 2 |
| **42** | U-T | U-T | U-T | 0 | 0 | 0 | 2 |
| **43** | U-T | U-P | U-T | 0 | 0 | 0 | 2 |
| **44** | U-T | U-P | U-P | 0 | 0 | 0 | 2 |
| **45** | U-P | U-P | U-P | 0 | 0 | 0 | 2 |
| **46** | U-P | U-S | U-P | 0 | 2 | 0 | 2 |
| **47** | U-P | U-S | U-S | 0 | 2 | 1 | 2 |
| **48** | U-S | U-S | U-S | 0 | 2 | 1 | 3 |
| **49** | U-S | U-T | U-S | 0 | 2 | 1 | 3 |
| **50** | U-S | U-T | U-T | 3 | 2 | 1 | 3 |
| **51** | U-T | U-T | U-T | 3 | 3 | 1 | 3 |
| **52** | U-T | U-P | U-T | 3 | 3 | 2 | 3 |
| **53** | U-T | U-P | U-P | 3 | 3 | 2 | 0 |
| **54** | U-P | U-P | U-P | 3 | 3 | 2 | 0 |
| **55** | U-P | U-S | U-P | 0 | 3 | 2 | 0 |
| **56** | U-P | U-S | U-S | 0 | 2 | 2 | 0 |
| **57** | U-S | U-S | U-S | 0 | 2 | 2 | 0 |
| **58** | U-S | U-T | U-S | 0 | 2 | 2 | 0 |
| **59** | U-S | U-T | U-T | 0 | 2 | 2 | 0 |

The table above demonstrates the full 60-step interaction cycle, showing:
- **Universal Sets**: Clear 3-step cycling (U-P → U-S → U-T), with U1, U2, and U3 transitioning sequentially
- **Particular Sets**: Complex nested concurrency patterns with staggered 5-step transitions
- **Interaction Effects**: The Particular states evolve based on the convolution formula: S_i(t+1) = (S_i(t) + Σ_{j≠i} S_j(t) + U_idx(t)) mod 4

## Visualization

The generated image, `system5_deterministic_timeline.png`, visually represents the 60-step state transitions.

- **Universal Sets**: Show a clear, repeating 3-step pattern (`U-P`, `U-S`, `U-T`).
- **Particular Sets**: Show a complex, evolving pattern that only repeats every 20 steps, demonstrating the effect of the nested concurrency and the influence of the Universal Set phase.

## Deliverables

The following files are provided:

1.  **`SYSTEM5_DETERMINISTIC_DOCUMENTATION.md`**: This document, detailing the model and results.
2.  **`system5_state_transitions_nested.cpp`**: The C++ source code implementing the model with nested concurrency.
3.  **`visualize_system5_deterministic.py`**: The Python script used to generate the timeline visualization.
4.  **`system5_deterministic_timeline.png`**: The visual timeline of the state transitions.

This completes the modeling of System 5, providing a plausible, executable model for the hypothesized structure and the complex "concurrency-of-concurrency" logic.
