# Cost & Consensus Benchmark: Deterministic vs Intelligent Contracts on Testnet Bradbury

**Author:** hieudao151093 (Portal: Solomon) · Wallet: `0x932CB99F3Da36A0Fbb6928248FF043b93FB88C9b`
**Network:** GenLayer Testnet Bradbury (Phase 1) · **Date:** June 2026
**Companion repo:** https://github.com/hieudao151093/genlayer-studio-vs-bradbury

---

## Abstract

Standard blockchain benchmarks (TPS, raw gas) describe deterministic execution and break down
on GenLayer, where Intelligent Contracts invoke an LLM and reach finality through Optimistic
Democracy. This is an empirical, fully on-chain-verifiable benchmark of the **execution cost and
consensus behavior gap** between a deterministic contract and an Intelligent Contract, measured
with the same wallet on Testnet Bradbury. Every figure links to a public GenLayer Explorer
transaction — no synthetic data. It closes with concrete, specification-level enhancement
proposals.

---

## 1. Methodology

Two contracts were deployed and exercised on Bradbury from the same wallet in the same session,
isolating a single variable — whether execution invokes an LLM:

- **Control (deterministic):** `storage.py` — a plain key/value contract with no LLM call.
- **Treatment (Intelligent Contract):** `llm_erc20.py` — an ERC-20 whose `transfer` method
  sends a prompt to an LLM to validate the transaction, then resolves via consensus.

For each, I recorded the finality status, the consensus path (from the explorer's Transaction
Journey), and the on-chain cost (L2 transaction count, gas, fee). Contract source for both is in
the companion repo and is reproducible by anyone with a funded Bradbury wallet.

---

## 2. Results

| Metric | `storage` (deterministic) | `llm_erc20.transfer` (Intelligent) |
|---|---|---|
| Finality status | **ACCEPTED** | **UNDETERMINED** |
| Time to outcome | ~immediate | ~108 s (13:55:17 → 13:57:05) |
| Consensus steps | minimal | **22-step journey** (2 full rounds) |
| Leader rotations | 0 | ≥ 2 |
| Appeals triggered | 0 | **1 (automatic)** |
| Underlying L2 transactions | trivial | **48** |
| Gas | trivial | **27,854,311** |
| Compute fee | ~0 | **0.00254736 GEN** |
| LLM output correctness | n/a | **Correct** (`transaction_success: true`) |

**On-chain proof:**
- storage contract — `0xE54D423D0617dA51D62E533EFfaA86604907a22E`
  ([explorer](https://explorer-bradbury.genlayer.com/address/0xE54D423D0617dA51D62E533EFfaA86604907a22E))
- llm_erc20 contract — `0x733980D4C8eFFE7608423eA24a94705a2E0EDB31`
  ([explorer](https://explorer-bradbury.genlayer.com/address/0x733980D4C8eFFE7608423eA24a94705a2E0EDB31))
- transfer tx (UNDETERMINED) — `0xe158f417...ceeef5`
  ([explorer](https://explorer-bradbury.genlayer.com/tx/0xe158f417e00336ba372f648523a78df0cdd72a17b855745385d996a716ceeef5))

---

## 3. Analysis

### 3.1 The cost gap is structural, not incidental

A single `transfer` expanded into **48 L2 transactions and ~27.9M gas**, versus a near-zero
deterministic baseline. The cost does not come from the token logic (a balance update is cheap);
it comes from the **non-deterministic block** — the LLM call plus the multi-round commit/reveal
voting that each validator must run and that the protocol must record on-chain. Any TPS or
gas-per-call figure for GenLayer is therefore meaningless unless it states whether the contract
is deterministic or LLM-invoking; the two differ by more than an order of magnitude.

### 3.2 A correct LLM answer is not sufficient for finality

The most important finding. The transaction's `Output Data` returned
`{"transaction_success": true, "transaction_error": "", "updated_balances": {...}}` — the LLM
evaluated the transfer correctly and produced valid updated balances. Yet the transaction
finalized as **UNDETERMINED**, even after an automatic appeal and a second full consensus round.
Correctness of the model output and finality of the transaction are **decoupled**: finality
requires enough validators to independently converge, which the Phase-1 validator set did not
reach for this call.

### 3.3 Optimistic Democracy is observable, and its failure mode is visible

The 22-step journey (`Leader proposal → Vote commit → Leader reveal → Vote reveal → leader
rotated → … → Decided: Undetermined → Appeal Submitted → … → Decided: Undetermined`) shows the
protocol behaving exactly as designed under non-convergence: it rotates leaders and escalates to
appeal rather than forcing a wrong verdict. The failure mode is *safe* (no incorrect finality)
but *unproductive* (no finality at all), and on a small validator set it appears reachable with a
single ordinary LLM call.

---

## 4. Proposed enhancements (specifications)

1. **Surface a determinism class in contract metadata.** Add an optional `execution_class`
   hint (`deterministic` | `llm`) the explorer and Studio can display, so cost and latency
   expectations are set before a user signs. Rationale: §3.1 shows the two classes are not
   comparable; users currently learn this only after a 48-tx surprise.

2. **Expose a convergence score on UNDETERMINED transactions.** When a tx finalizes UNDETERMINED,
   record the closest vote distribution reached (e.g. 4/7 agree) in the receipt. Rationale: §3.2
   — distinguishing "validators split 4/3" from "no signal" tells builders whether to retry,
   raise temperature constraints, or tighten the prompt.

3. **Prompt-determinism guidance for Intelligent Contracts.** Document a recommended pattern for
   LLM-invoking methods (low temperature, strict JSON schema, deterministic pre-formatting of
   inputs) to raise inter-validator agreement. `llm_erc20.transfer` already pre-formats inputs
   deterministically before the non-det block; measuring agreement with vs without this step is a
   natural follow-up benchmark.

4. **Bounded-retry helper.** A standard contract/SDK helper that re-submits an UNDETERMINED call
   up to N times with backoff, so application developers are not left hand-rolling retry logic
   around a probabilistic finality model.

---

## 5. Reproducibility & limitations

**Reproduce:** fund a Bradbury wallet (faucet, 100 GEN/7 days, requires 0.01 ETH mainnet),
deploy the two contracts from the companion repo to Bradbury, call `llm_erc20.transfer`, and
read the explorer Transaction Journey. Full steps in the repo README.

**Limitations:** this is a single-call observation on Testnet Bradbury Phase 1 with a limited
validator set; absolute figures (gas, step count, undetermined rate) will shift as the validator
set and model routing mature. The *direction* of the findings — Intelligent Contract calls are
structurally far heavier, and finality is decoupled from LLM correctness — is expected to hold.
A useful extension is an N-trial run to estimate the UNDETERMINED rate and gas distribution
rather than a point sample.
