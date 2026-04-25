# 🧪 LLM Temperature Benchmark — Homelab Experiment

A quick experiment testing how **temperature** affects output quality and latency on a small local model (`qwen:0.5b`), using a straightforward AWS networking question as the prompt.

---

## Experiment Setup

| Parameter | Value |
|-----------|-------|
| Model | `qwen:0.5b` |
| Prompt | *"What is the difference between private and public subnet in AWS? Explain in 3 lines"* |
| Temperatures tested | `0.1`, `0.7`, `1.5` |
| Runs | 3 |

---

## Results

### Run 1

| Temperature | Latency | Output Summary |
|-------------|---------|----------------|
| 0.1 | 3.40s | Defines private/public subnets as "owned by individual/org" — factually incorrect |
| 0.7 | 3.77s | References 网关ID (gateway ID in Chinese) — off-topic, partially incoherent |
| 1.5 | 1.43s | Mixed English/Chinese output, vague and incomplete |

### Run 2

| Temperature | Latency | Output Summary |
|-------------|---------|----------------|
| 0.1 | 4.68s | Best output of all runs — closest to a correct definition |
| 0.7 | 1.91s | Incorrect — claims private subnets are *created within* public subnets |
| 1.5 | 2.24s | Mixed Chinese characters, factually wrong |

### Run 3

| Temperature | Latency | Output Summary |
|-------------|---------|----------------|
| 0.1 | 4.14s | Incorrect — frames the difference as "high-speed vs low-speed internet" |
| 0.7 | 2.60s | Partially relevant but introduces unrelated SAC permissions concept |
| 1.5 | 3.01s | Confused — says private subnets have a "limited number of public subnets" |

---

## Observations

- **Low temperature (0.1)** produced the most consistent outputs but was still factually wrong in 2 out of 3 runs. Latency was generally higher (~4s).
- **Mid temperature (0.7)** showed high variance — one near-correct answer, two nonsensical ones.
- **High temperature (1.5)** was the worst across the board — outputs mixed languages, were incoherent, and occasionally faster (possibly cutting off early).
- **`qwen:0.5b` is too small** for factual AWS/networking questions — it hallucinates confidently and consistently.

---

## Next Steps

- [ ] Repeat with a larger model (e.g. `qwen:1.8b`, `llama3.2:1b`, `mistral:7b`) to compare quality at same temperatures
- [ ] Add a correct reference answer to score outputs objectively
- [ ] Test with a more open-ended prompt to see if small models perform better without factual constraints
- [ ] Automate scoring (e.g. cosine similarity or LLM-as-judge) across runs

---

## Environment

- **Platform:** Homelab (Raspberry Pi / k3s)
- **Inference:** Ollama (local)
- **Date:** April 2026
