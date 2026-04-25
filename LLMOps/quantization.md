# LLM Parameters & Quantization — Session Recap

> A quick refresher on what parameters are, how floating-point and quantization work, and how to size LLMs for your hardware.

---

## 1. What is a parameter?

- A **parameter** is one floating-point number inside the neural network — a learned weight or bias.
- Training = nudging billions of these numbers up/down so predictions get less wrong.
- The "intelligence" of an LLM lives entirely in the specific values these numbers settle on.
- Mental model: a billion-knob mixing board. No single knob matters; the pattern across all of them does.

## 2. Naming conventions

| Name | Parameter count | Meaning |
|---|---|---|
| **nanoGPT 85k** | 85,000 | Karpathy's tiniest teaching config. Can't speak English. Demonstrates architecture only. |
| **ollama:0.5b** | 500 million | The `:Xb` suffix is always parameter count in billions. |
| **TinyLlama** | 1.1 billion | Llama 2 architecture, shrunk, pretrained on 3T tokens. Runs on a Pi. |
| **7B / 13B / 70B** | 7B / 13B / 70B | Standard size tiers in the open-source ecosystem. |

## 3. Floating-point formats

Each parameter is stored using a fixed number of bits:

| Format | Bits | Bytes/param | Use case |
|---|---|---|---|
| fp32 | 32 | 4 | Original training, "full precision" |
| fp16 | 16 | 2 | Standard inference baseline |
| bf16 | 16 | 2 | Training (more range, less precision) |
| int8 | 8 | 1 | Light quantization |
| int4 | 4 | 0.5 | Aggressive quantization (default for local LLMs) |

Format = `sign bit + exponent + mantissa`. It's binary scientific notation.

## 4. Bit math (the foundation)

**N bits → 2ᴺ possible values.** Each new bit doubles the choices.

| Bits | Values |
|---|---|
| 4 | 16 |
| 8 | 256 |
| 16 | 65,536 |
| 32 | ~4.3 billion (IPv4 space — and we ran out) |
| 128 | ~3.4 × 10³⁸ (IPv6 — never running out) |

The exact same bit-budget logic shows up across all infrastructure: RAM sizing, hash collisions, UUID uniqueness, color depth, Bloom filters.

## 5. Quantization — what & why

**What:** Lossy compression of weights. Round each weight to one of a small fixed set of values, store just the index.

**Why it works:** Redundancy. Billions of weights cooperate; small rounding errors in each one mostly cancel. Like a choir with one slightly off-pitch singer — the rest cover.

**Best analogy:** JPEG, but for model weights. ~4× smaller file, ~95% of the quality.

**Why int4 wins for local LLMs:**
1. Memory is the wall — int4 lets a 7B model fit in ~4 GB instead of 14 GB
2. Bandwidth is also a wall — fewer bits per weight = faster inference
3. Quality holds up — int4 is the last stop before benchmarks fall off a cliff (int3, int2 collapse)

**Big rule:** A bigger model at lower precision usually beats a smaller model at higher precision *for the same memory footprint*. 13B-int4 generally outperforms 7B-fp16, and uses half the RAM.

## 6. Memory sizing — Pi 5 (8 GB) worked example

Raw weight math:

| Model | fp16 size | int4 size |
|---|---|---|
| 7B | 14 GB ❌ | 3.5 GB ✅ |
| 13B | 26 GB ❌ | 6.5 GB ⚠️ |
| TinyLlama (1.1B) | 2.2 GB | 0.7 GB ✅ |

**But raw weights ≠ runtime memory.** Real total = weights + OS + runtime + KV cache:

- OS (Pi OS): ~0.5–1 GB
- Ollama / llama.cpp runtime: a few hundred MB
- **KV cache** (scales with context length): 1–2 GB for a 13B at 4K context
- Activation memory during forward pass

**Rule of thumb:** Budget **1.3–1.5× the raw weight size** for actual runtime use. More for long contexts.

So on the 8 GB Pi 5:
- 7B-int4: 3.5 GB × 1.5 ≈ 5.3 GB used → **fits comfortably**
- 13B-int4: 6.5 GB + 1.5 GB OS + 1–2 GB KV ≈ 9–10 GB → **OOMs or swaps to SD card**

## 7. Why ~4 GB and not 3.5 GB for 7B-int4 in practice?

A real `Q4_K_M.gguf` for Llama-2-7B is ~4.08 GB, not 3.5 GB. Two reasons:

1. **Per-block scale metadata.** Quantization needs to store the scale factor (where the grid sits) at higher precision per block of weights. Adds ~0.5 effective bits/weight.
2. **Mixed precision.** Critical layers (embeddings, output projection, parts of attention) are kept at higher precision (Q6/Q8) because they hurt quality the most when squashed.

The pure `Q4_0` variant *does* land closer to 3.6 GB but with measurably worse output. File size vs perplexity tradeoff sitting in plain sight.

---

## Gotchas to remember

- **Model file size ≠ runtime memory.** Forget the KV cache and you'll get paged at 3 AM.
- **KV cache scales with context length** — doubling the context window can blow your memory budget.
- **"Quantization" colloquially means below fp16.** fp16 itself is technically already quantized from fp32; just don't call it that in conversation.
- **Per-block scale metadata** is why real GGUF files run a bit larger than naive bit math suggests.
- **Tiny models degrade harder** under aggressive quantization — less redundancy, fewer singers in the choir.
- **int2/int3 = quality cliff.** Don't go below int4 unless you really know why.

## Open threads / next sessions

- [ ] How does quantization actually pick the grid points? (Not evenly spaced — k-means-style or learned.)
- [ ] Why can't we train directly in int4? What does training need from a number format that inference doesn't?
- [ ] KV cache deep dive — what is it actually caching, and why does context length cost so much memory?
- [ ] Distributed inference across multiple Pis (sharding model layers across nodes)
- [ ] How GGUF format actually lays out weights on disk (relevant if you ever want to write LLMOps tooling)

## Mental model to carry forward

> **Parameters → bits per parameter → memory → hardware → cost & latency.**
>
> That single chain explains 80% of inference-side LLMOps decisions.
