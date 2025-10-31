import csv
import hashlib
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

class SHA256PRNG:
    def __init__(self, seed: str):
        self.state = hashlib.sha256(seed.encode('utf-8')).digest()

    def randbelow(self, n: int) -> int:
        if n <= 0:
            raise ValueError("n must be positive")
        while True:
            self.state = hashlib.sha256(self.state).digest()
            val = int.from_bytes(self.state[:8], 'big')
            limit = (1 << 64) - ((1 << 64) % n)
            if val < limit:
                return val % n

@dataclass
class FluxTickets:
    flux_id: str
    tickets: int

class WeightedPool:
    def __init__(self, entries: List[FluxTickets]):
        self.entries = [e for e in entries if e.tickets > 0]
        self._recompute_cumulative()

    def _recompute_cumulative(self):
        self.cumulative: List[Tuple[int, str]] = []
        total = 0
        for e in self.entries:
            total += e.tickets
            self.cumulative.append((total, e.flux_id))
        self.total_tickets = total

    def remove_flux(self, flux_id: str):
        self.entries = [e for e in self.entries if e.flux_id != flux_id]
        self._recompute_cumulative()

    def pick(self, randbelow_fn) -> Optional[str]:
        if self.total_tickets <= 0:
            return None
        roll = randbelow_fn(self.total_tickets)
        lo, hi = 0, len(self.cumulative) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if roll < self.cumulative[mid][0]:
                hi = mid
            else:
                lo = mid + 1
        return self.cumulative[lo][1]

def parse_months(term: str) -> int:
    s = str(term).strip().lower()
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif num:
            break
    months = int(num) if num else 0
    if "y" in s or "year" in s:
        return months * 12
    return months

def read_participants(file_obj) -> Dict[str, int]:
    file_obj.seek(0)
    reader = csv.DictReader((line.decode('utf-8-sig') if isinstance(line, bytes) else line for line in file_obj))
    field_map = {k.strip().lower(): k for k in (reader.fieldnames or [])}
    flux_key = field_map.get("flux_id") or field_map.get("fluxid") or field_map.get("flux id")
    months_key = field_map.get("months")
    term_key = field_map.get("term")
    if not flux_key or (not months_key and not term_key):
        raise ValueError("CSV must include 'flux_id' and either 'months' or 'term' column.")
    totals: Dict[str, int] = {}
    for row in reader:
        flux = (row.get(flux_key) or "").strip()
        if not flux:
            continue
        if months_key and (row.get(months_key) not in (None, "")):
            try:
                m = int(str(row[months_key]).strip())
            except ValueError:
                m = 0
        else:
            m = parse_months(str(row.get(term_key, "")))
        if m <= 0:
            continue
        totals[flux] = totals.get(flux, 0) + m
    return totals

def read_exclusions(file_obj) -> set:
    file_obj.seek(0)
    reader = csv.DictReader((line.decode('utf-8-sig') if isinstance(line, bytes) else line for line in file_obj))
    field_map = {k.strip().lower(): k for k in (reader.fieldnames or [])}
    flux_key = field_map.get("flux_id") or field_map.get("fluxid") or field_map.get("flux id")
    if not flux_key:
        raise ValueError("Exclude CSV must include a 'flux_id' column.")
    excluded = set()
    for row in reader:
        flux = (row.get(flux_key) or "").strip()
        if flux:
            excluded.add(flux)
    return excluded

def run_raffle(totals: Dict[str, int], prizes: int, seed: Optional[str] = None):
    entries = [FluxTickets(fid, tix) for fid, tix in totals.items() if tix > 0]
    if not entries:
        raise ValueError("No valid participants after processing.")
    if seed:
        rng = SHA256PRNG(seed)
        randbelow_fn = rng.randbelow
        rng_mode = f"deterministic (seed='{seed}')"
    else:
        import secrets
        randbelow_fn = secrets.randbelow
        rng_mode = "cryptographically strong (secrets)"
    pool = WeightedPool(entries)
    winners: List[str] = []
    for _ in range(prizes):
        pick = pool.pick(randbelow_fn)
        if pick is None:
            break
        winners.append(pick)
        pool.remove_flux(pick)
    totals_sorted = sorted(entries, key=lambda e: e.tickets, reverse=True)
    return {
        "rng_mode": rng_mode,
        "participants": len(entries),
        "tickets": sum(e.tickets for e in entries),
        "winners": winners,
        "top10": [(e.flux_id, e.tickets) for e in totals_sorted[:10]],
    }
