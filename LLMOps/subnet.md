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

## Raw Outputs

<details>
<summary><strong>Run 1</strong></summary>

**Temperature: 0.1** *(Latency: 3.40s)*
> Private Subnet: A private subnet is a subnets that are owned by an individual or organization. Private Subnets are used for security reasons, such as protecting against unauthorized access.
> Public Subnet: A public subnet is a subsubnet that is owned by the same entity or organization as the primary subnet. Public Subnets are used for business purposes, such as providing access to data and services.

**Temperature: 0.7** *(Latency: 3.77s)*
> Private Subnet: In a private subnet, the network ID (网关ID) is assigned to each device connected to it. This allows devices to communicate with each other directly without requiring them to connect through a security group.
> Public Subnet: In a public subnet, the network ID (网关ID) is assigned to each device connected to it. This allows devices to communicate with each other more easily, but may require additional management resources.

**Temperature: 1.5** *(Latency: 1.43s)*
> Private subnets are reserved for specific use cases, such as data processing or remote work. Public subnet则是用来承载任何类型的数据和流量。

</details>

<details>
<summary><strong>Run 2</strong></summary>

**Temperature: 0.1** *(Latency: 4.68s)*
> Private Subnet: A private subnet is a set of IP addresses that are reserved for use within a specific network. Private Subnets are used to protect sensitive information or resources from unauthorized access.
> Public Subnet: A public subnet is a set of IP addresses that are available for use within a specific network. Public Subnets are used to share resources, such as storage or computing power, among multiple users.
> In summary, private subnets are reserved for use within a specific network, while public subnets are available for use within a specific network.

**Temperature: 0.7** *(Latency: 1.91s)*
> Private subnets are created within a public subnet. Public subnets, on the other hand, are created by an individual user or organization. Therefore, private subnets have a higher level of control over their resources.

**Temperature: 1.5** *(Latency: 2.24s)*
> Private subnets are managed by a cloud service provider, while public subnets can be owned, purchased, or租 out.
> In summary, private subnets are managed by cloud service providers, while public subnets can be owned, purchased, or租 out.

</details>

<details>
<summary><strong>Run 3</strong></summary>

**Temperature: 0.1** *(Latency: 4.14s)*
> Private Subnet: A private subnet is a set of IP addresses that are used to connect to a private network. Private Subnets are typically used for high-speed internet connections.
> Public Subnet: A public subnet is a set of IP addresses that are used to connect to a public network. Public Subnets are typically used for low-speed internet connections.
> In summary, private subnets are used for high-speed internet connections, while public subnets are used for low-speed internet connections.

**Temperature: 0.7** *(Latency: 2.60s)*
> In AWS, a private subnet refers to a virtual network within an individual cloud. A public subnet refers to a group of private subnets within an individual cloud.
> The main difference between private and public Subnets is the level of visibility it provides for applications that require security access control (SAC) permissions.

**Temperature: 1.5** *(Latency: 3.01s)*
> Private subnets have a limited number of public subnets. Public subnets are free to join, while private subnets require specific conditions such as being an operator on the network or having a specified level of access control.
> In summary, private subnets have a limited number of public subnets, while public subnets are free to join.

</details>

---

## Environment

- **Platform:** Homelab (Raspberry Pi / k3s)
- **Inference:** Ollama (local)
- **Date:** April 2026
