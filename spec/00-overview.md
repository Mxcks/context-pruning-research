# Overview: Context Pruning via Tagging-Based Retention

## Core Thesis

**Tagging is superior to scoring for context selection because it replaces opaque approximation with auditable structure.**

Scoring systems attempt to quantify "importance" through continuous numerical weights. This approach has inherent limitations:

1. **Hidden logic**: The weights are produced by a model or heuristic that may vary unpredictably
2. **No reversibility**: Once discarded by a lower score, relevance is irrecoverable 
3. **Leaky composition**: Scores from different domains don't compose — comparing domain email with domain math through a single global ranking mixes unrelated contexts
4. **User blindness**: A user cannot inspect or adjust an opaque scoring system

Tagging systems avoid these problems through:

- **Explicit categorization**: Each entry belongs to exactly one lifecycle domain
- **Deterministic rules**: Tag → rule mapping is invariant and auditable
- **First-class addressing**: Detached entries remain addressable by name
- **Composable boundaries**: Domains can be toggled as atomic units without bleeding

## Why This Matters Now

Current long-context strategies follow three patterns, each with fundamental flaws:

| Approach | How It Selects | Failure Mode |
|----------|---------------|--------------|
| Window-based retention | Recency (last N turns) | Early critical context lost |
| Heuristic scoring | Relevance to current query | Unauditable, inconsistent |
| Aggressive summarization | All-of-the-above | Precision destruction |

Context pruning introduces a fourth: **tag-driven lifecycle management**. Information is never "lost" — it transitions from active → compressed → detached → garbage-collected through explicit rules. The agent can re-activate any context by reference name at any time.

## Key Design Decisions

1. **Tags replace scores**: Selection is categorical, not continuous
2. **Packages are primitives**: Information enters/leaves the window as bundles, not individual items
3. **Compression is lazy**: Only applied to tags that say `transform/compression-capable`
4. **Garbage collection is bounded**: TTL-based cleanup prevents accumulation of stale metadata

## Related Work

- Prompt compression (e.g., LLMLingua)
- Context window management patterns
- Hierarchical memory for agents
- Retrieval Augmented Generation (RAG) systems

Context pruning differs from these by treating the **selection mechanism itself as a tagging lifecycle** rather than a compression or retrieval problem.
