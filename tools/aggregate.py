from langchain.tools import tool

@tool
def merge_and_rank_flight_offers(all_offers: list[list[dict]], top_k: int):
    """
    Merge and rank flight offers from multiple searches into one global ranking.

    Use this tool after calling search_flights_amadeus multiple times (e.g., nearby dates).
    Input all_offers = [offers_from_call_1, offers_from_call_2, ...]
    Output is the globally cheapest top_k offers across all calls.
    """
    flat: list[dict] = []
    for batch in all_offers:
        if batch:
            flat.extend(batch)

    def signature(o: dict) -> str:
        price = (o.get("price") or {}).get("grandTotal") or ""
        validating = ",".join(o.get("validatingAirlineCodes") or [])
        parts = [validating, str(price)]
        for it in o.get("itineraries", []):
            segs = it.get("segments", [])
            seg_sig = "|".join(
                f"{s.get('departure', {}).get('iataCode','')}-"
                f"{s.get('arrival', {}).get('iataCode','')}@"
                f"{s.get('departure', {}).get('at','')}"
                for s in segs
            )
            parts.append(seg_sig)
        return "||".join(parts)

    seen = set()
    deduped = []
    for o in flat:
        sig = signature(o)
        if sig not in seen:
            seen.add(sig)
            deduped.append(o)

    deduped.sort(key=lambda o: float((o.get("price") or {}).get("grandTotal") or "999999999"))
    return deduped[:top_k]