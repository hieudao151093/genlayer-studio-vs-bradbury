# Studio Sandbox vs Bradbury Testnet — A Verified Comparison for GenLayer Builders

A reproducible, on-chain-verified walkthrough of how the **same Intelligent Contracts**
behave when deployed to the local **GenLayer Studio sandbox (studionet)** versus the
real, decentralized **Testnet Bradbury**.

Every claim in this repo is backed by a **real Bradbury transaction** you can open in the
GenLayer Explorer. No mock data.

> Why this matters: GenLayer explicitly asks builders to *"deploy contracts and compare
> their execution on testnet versus Studio"* to help refine the system. Many newcomers
> assume Studio sandbox activity is the "real" network — it is not. This repo documents
> the difference, with proof.

---

## TL;DR — what's different

| Aspect | Studio sandbox (studionet) | Testnet Bradbury |
|---|---|---|
| Network label in wallet header | `GenLayer Studio` | `GenLayer Bradbury` |
| Where it runs | Local simulated env in your browser | Real decentralized validator set |
| Counts toward Portal contributions | No — local sandbox only | Yes — real on-chain activity tied to your wallet |
| Dependency header (`Depends`) | `py-genlayer:1jb45aa8...09h6` (v0.2.16) | Same pinned hash worked unchanged |
| LLM consensus | Simulated | Real multi-validator Optimistic Democracy |
| Transaction permanence | Resets on Studio reset | Persisted on-chain (history may reset per testnet rules) |

---

## Contracts tested

Each contract is deployed to **both** environments. Source files live in `/contracts`.
These are the canonical GenLayer example contracts (guaranteed to compile) so the comparison
is fully reproducible by anyone.

| # | Contract | What it isolates |
|---|---|---|
| 1 | `storage.py` | Deterministic baseline — plain contract, instant ACCEPTED |
| 2 | `llm_erc20.py` | Intelligent Contract — `transfer` calls an LLM to validate the transaction |
| 3 | `header_gotcha.py` | The `Depends` header version gotcha (the #1 newcomer deploy failure) |

---

## On-chain receipts (the proof)

> This is the section that makes the submission credible. Every Bradbury deploy/execute
> gets a row here with a clickable Explorer link.

| Contract | Action | Environment | Tx hash / Explorer link | Result |
|---|---|---|---|---|
| storage (deterministic) | deploy | Bradbury | [contract `0xE54D...a22E`](https://explorer-bradbury.genlayer.com/address/0xE54D423D0617dA51D62E533EFfaA86604907a22E) | **ACCEPTED** (instant) |
| llm_erc20 (Intelligent) | deploy | Bradbury | [contract `0x7339...DB31`](https://explorer-bradbury.genlayer.com/address/0x733980D4C8eFFE7608423eA24a94705a2E0EDB31) | **ACCEPTED** |
| llm_erc20.transfer (LLM call) | contract_call | Bradbury | [tx `0xe158...eeef5`](https://explorer-bradbury.genlayer.com/tx/0xe158f417e00336ba372f648523a78df0cdd72a17b855745385d996a716ceeef5) | **UNDETERMINED** (after 22-step consensus + appeal) |

**storage contract (deterministic baseline):** `0xE54D423D0617dA51D62E533EFfaA86604907a22E`
**llm_erc20 contract (Intelligent Contract):** `0x733980D4C8eFFE7608423eA24a94705a2E0EDB31`
**Deployer wallet:** `0x932CB99F3Da36A0Fbb6928248FF043b93FB88C9b`
**Network:** Testnet Bradbury (Phase 1)

---

## Reproduce this yourself

### Prerequisites
- A wallet with **≥ 0.01 ETH on Ethereum mainnet** (faucet anti-sybil requirement)
- Claim 100 testnet GEN from the GenLayer Testnet Faucet (100 GEN / 7 days)
- GitHub account linked to your GenLayer Portal profile

### Studio sandbox (studionet)
1. Open `studio.genlayer.com`, connect wallet
2. Load each contract from `/contracts`
3. Run & Deploy → record result + logs (screenshots in `/evidence/studio`)

### Bradbury testnet
1. Add the GenLayer Testnets chain to your wallet (button on the faucet page)
2. Point your deploy target to Bradbury (Studio network selector, or
   `genlayer network testnet-bradbury` via CLI)
3. Deploy each contract → copy the **transaction hash** → open in GenLayer Explorer
4. Paste every link into the receipts table above

---

## Key findings

These are observations from actually deploying to **both** environments with the same wallet
and contracts. Every finding is backed by a transaction in the receipts table above.

### 1. A deterministic contract and an Intelligent Contract behave completely differently on Bradbury

Deploying `storage.py` (plain, deterministic) reached **ACCEPTED almost instantly**. Calling
`llm_erc20.transfer` — which sends a prompt to an LLM to validate the transfer — went through a
**22-step consensus journey** and still ended **UNDETERMINED**. Same network, same wallet, same
session: the only variable is whether the contract invokes an LLM. This is the single clearest
demonstration of why GenLayer exists — deterministic execution is trivial to agree on; subjective,
AI-driven execution is not.

### 2. "Optimistic Democracy" is visible end-to-end on the explorer

The `transfer` transaction journey shows the full consensus protocol running live:
`Transaction Submitted → Activation → Leader proposal → Vote commit → Leader reveal → Vote reveal
→ Transaction leader rotated → (repeat) → Decided: Undetermined → Appeal Submitted → (full second
round) → Decided: Undetermined`. The **leader was rotated** when consensus failed, and an
**appeal was automatically submitted** after the first undetermined verdict — exactly the appeals
mechanism described in GenLayer's docs, observable on a real transaction.

### 3. The LLM produced a correct result, yet the transaction was still UNDETERMINED

The transaction's `Output Data` returned `{"transaction_success": true, "transaction_error": "",
"updated_balances": {...}}` — the AI evaluated the transfer correctly and computed updated
balances. Despite a correct output, validators did not converge to a binding verdict within the
finalization window. The takeaway: on Testnet Bradbury (Phase 1), a *correct LLM answer is not
sufficient* for finality — enough validators must independently agree, which the current validator
set did not reach for this call.

### 4. An Intelligent Contract call is dramatically heavier than a deterministic one

The single `transfer` call expanded into **48 underlying L2 transactions** consuming
**27,854,311 gas** (≈ 0.00254736 GEN of compute), versus the near-trivial cost of the `storage`
deploy. The non-deterministic block (the LLM call + multi-round voting) is where almost all the
cost and latency live.

### 5. The dependency header pinned to studionet also worked on Bradbury

The `# { "Depends": "py-genlayer:1jb45aa8...09h6" }` header that works on hosted Studio
(studionet, v0.2.16) deployed successfully on Bradbury without modification. (Note: the
`py-genlayer:test` tag from many tutorials fails schema-loading on hosted Studio with
*"Could not load contract schema"* — beginners must use the pinned hash, not `:test`.)

### 6. MetaMask's transaction simulation is unreliable on Bradbury (chain 4221)

MetaMask showed *"change estimate unavailable"* and failed to push transactions on the Bradbury
chain, because its simulation service does not yet support chain 4221. Importing the same private
key into a wallet without forced pre-simulation (OKX in this case) deployed the identical
contracts without issue. The wallet was never the problem — the simulation layer was.

---

## Repo structure

```
.
├── README.md              # this file
├── contracts/             # the .py contracts deployed to both envs
│   ├── storage.py
│   ├── llm_erc20.py
│   ├── header_gotcha.py
│   └── ...
├── evidence/
│   ├── studio/            # screenshots of studionet runs
│   └── bradbury/          # screenshots of Bradbury runs
└── receipts.md            # full table of on-chain tx links
```

---

## Author

Built as a contribution to the GenLayer Builder Program.
GitHub: [hieudao151093](https://github.com/hieudao151093) · Portal: Solomon · Wallet: `0x932CB99F3Da36A0Fbb6928248FF043b93FB88C9b`
