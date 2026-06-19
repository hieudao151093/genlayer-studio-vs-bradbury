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
| Counts toward Portal contributions | _<fill in after testing>_ | _<fill in after testing>_ |
| Dependency header (`Depends`) | `py-genlayer:<studionet hash>` | `py-genlayer:<bradbury hash>` _(verify — may differ)_ |
| LLM consensus | Simulated | Real multi-validator Optimistic Democracy |
| Transaction permanence | Resets on Studio reset | Persisted on-chain (history may reset per testnet rules) |

_(Fill each row from your own deployments. Replace every "fill in" with a real observation
+ a transaction link.)_

---

## Contracts tested

Each contract is deployed to **both** environments. Source files live in `/contracts`.
These are the canonical GenLayer example contracts (guaranteed to compile) so the comparison
is fully reproducible by anyone.

| # | Contract | What it isolates |
|---|---|---|
| 1 | `storage.py` | Deterministic baseline — does a plain contract behave identically? |
| 2 | `llm_erc20.py` (or `wizard_of_coin.py`) | Non-determinism — real LLM consensus vs simulated |
| 3 | web-fetch example | Native web access behavior across environments |
| 4 | `header_gotcha.py` | The `Depends` header version gotcha (the #1 newcomer deploy failure) |

---

## On-chain receipts (the proof)

> This is the section that makes the submission credible. Every Bradbury deploy/execute
> gets a row here with a clickable Explorer link.

| Contract | Action | Environment | Tx hash / Explorer link | Result |
|---|---|---|---|---|
| storage | deploy | Bradbury | [`0x9e644fee...18bd63`](https://explorer-bradbury.genlayer.com/address/0xE54D423D0617dA51D62E533EFfaA86604907a22E) | ACCEPTED |
| storage | update_storage | Bradbury | `<paste tx link>` | accepted |
| llm_erc20 | deploy | Bradbury | `<paste tx link>` | accepted |
| wizard_of_coin | deploy | Bradbury | `<paste tx link>` | accepted |

**Deployed contract address (storage, Bradbury):** `0xE54D423D0617dA51D62E533EFfaA86604907a22E`
**Creator / deployer wallet:** `0x932CB99F3Da36A0Fbb6928248FF043b93FB88C9b`
**Deployment tx:** `0x9e644fee7c30326e72c1e31cf8226dac8896267f04998fc57a09c87f7f18bd63`
**Network:** Testnet Bradbury (Phase 1) · **Status:** ACCEPTED · **Fee:** 0.00 GEN

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

_(Write 4–6 concrete, specific findings here as you go. Examples of the shape:)_

1. **Dependency header is environment-specific.** The `py-genlayer:test` tag from tutorials
   fails schema-loading on hosted Studio (v0.2.16); the environment's pinned hash is
   required. Bradbury required `<X>`. _(Document the exact behavior you observed.)_
2. **LLM contracts diverge.** _(What you saw on real consensus vs sandbox.)_
3. ...

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
GitHub: `<your handle>` · Portal: `<your portal profile>`
