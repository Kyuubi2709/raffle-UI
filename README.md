# ⚡ FluxID Raffle UI

A lightweight, transparent raffle tool used for Flux community giveaways.  
Built with Flask + Docker, it runs fair draws where the number of tickets is based on **Kaspa Node deployments** verified through the Flux API.

**Live URL**: [raffleui.app.runonflux.io](https://raffleui.app.runonflux.io/)

---

## 🎯 Giveaway Rules

1. Each FluxID earns tickets based on the **subscription term** of their Kaspa Node deployment:

   | Subscription Term | Lottery Tickets |
   |-------------------|-----------------|
   | 1 month           | 1 ticket        |
   | 3 months          | 3 tickets       |
   | 1 year            | 12 tickets      |

2. If a FluxID has multiple deployments, the ticket count adds up.  
   _Example:_  
   - 6-month node = 6 tickets  
   - 1-month node = 1 ticket  
   → **Total: 7 tickets**

3. Only **one Nacho Kat NFT** can be won per FluxID.  
   Once a FluxID wins, all its tickets are removed from the pool for the next draws.

4. The raffle uses a **weighted random draw**, so entries with more months have higher chances, but every FluxID still has a shot.

---

## 🧾 Verifying the Ticket Data

https://api.runonflux.io/apps/globalappsspecifications

Search for apps with the deployment name **`KaspaNode`**.  
Each record corresponds to a FluxID and its node configuration.  
The data exported from this API forms the input spreadsheet for the raffle.

---

## 📊 Participant Data

The raffle reads a CSV file with two columns:

flux_id,months
1ABCxyz...,6
1DEFuvw...,1

**The official data export (`participants_giveaway1.csv`) is included in this repository.**

**The official data export (`exclude_giveaway1.csv`) is included in this repository.**

**The official data export (`participants_giveaway2.csv`) is included in this repository.**

**The official data export (`exclude_giveaway2.csv`) is included in this repository.**

- 1XcNTEsgVND4eb3bsVa2bjktnZZSruVct (Kyuubi94)
- 19S8wu3szFRaBhFgGwfZ4GRE4LUGfvsfNF (Kyuubi94)
- 196GJWyLxzAw3MirTT7Bqs2iGpUQio29GH (K.A.T)
- 0x79ef91a5b34c5d904172c938c2d3ebf3f7e6040f (Kyuubi94)

---

## 🧮 How the Raffle Works

- The backend computes total tickets per `flux_id`.
- Each ticket acts as a weighted entry in the pool.
- Winners are drawn one by one.
- After a FluxID wins, all its tickets are removed.
- The results page lists winners and top ticket holders for transparency.

The random number generator uses Python’s **cryptographically secure RNG**, or a deterministic seed for reproducible public draws.

---

## 🪙 Public Giveaway Reference

Official Giveaway_1 Tweet: https://x.com/Kaspa_KAT/status/1981768440797880356

Giveaway_1, Announcement of Winner + Seed to verify: https://x.com/Kaspa_KAT/status/1984629244186460161

Official Giveaway_2 Tweet: https://x.com/Kaspa_KAT/status/1985387044831465929

Giveaway_2, Announcement of Winner + Seed to verify: [LINK HERE]

---

## 🚀 Running Locally

### Docker (recommended)
```bash
docker build -t fluxid-raffle .
docker run --rm -p 8080:8080 fluxid-raffle
# then open http://localhost:8080
