import os
from langchain.tools import tool
from amadeus import Client
import time


@tool
def search_flights_amadeus(
    origin: str,
    destination: str,
    trip_type: str,  # "oneway" or "roundtrip"
    outbound_date: str,  # YYYY-MM-DD
    inbound_date: str | None,
    travel_class: str,  # ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
    baggage_included_only: bool,
    max_results: int,
    max_connections: int,
    max_total_minutes: int | None,
):
    """
    Search for flight prices using Amadeus and return the cheapest options.

    Parameters:
        - origin: IATA code of departure airport (e.g. GRU)
        - destination: IATA code of arrival airport (e.g. FCO)
        - trip_type: "oneway" or "roundtrip"
        - outbound_date: departure date (YYYY-MM-DD)
        - inbound_date: return date (YYYY-MM-DD), only used if trip_type is "roundtrip"
        - travel_class: ECONOMY, PREMIUM_ECONOMY, BUSINESS or FIRST
        - baggage_included_only: if true, return only flights with checked baggage included
        - max_results: number of flights to return
        - max_connections: maximum allowed connections per leg (0 = direct only)
        - max_total_minutes: maximum total flight duration per leg in minutes

    IMPORTANT:
    This tool only supports round trips where the return leg is destination → origin.
    For open-jaw trips (example: GRU → FCO and MXP → GRU),
    the LLM MUST call this tool twice as two one-way searches.
    """

    amadeus = Client(
        client_id=os.environ["AMADEUS_CLIENT_ID"],
        client_secret=os.environ["AMADEUS_CLIENT_SECRET"],
    )

    origin_destinations = [
        {
            "id": "1",
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDateTimeRange": {"date": outbound_date},
        }
    ]

    if trip_type == "roundtrip":
        origin_destinations.append(
            {
                "id": "2",
                "originLocationCode": destination,
                "destinationLocationCode": origin,
                "departureDateTimeRange": {"date": inbound_date},
            }
        )

    response = amadeus.shopping.flight_offers_search.post(
        {
            "currencyCode": "BRL",
            "originDestinations": origin_destinations,
            "travelers": [{"id": "1", "travelerType": "ADULT"}],
            "sources": ["GDS"],
            "searchCriteria": {
                "maxFlightOffers": max(50, max_results * 10),
                "flightFilters": {
                    "connectionRestriction": {
                        "maxNumberOfConnections": max_connections
                    },
                    "cabinRestrictions": [
                        {
                            "cabin": travel_class,
                            "coverage": "MOST_SEGMENTS",
                            "originDestinationIds": ["1"],
                        },
                        *(
                            [
                                {
                                    "cabin": travel_class,
                                    "coverage": "MOST_SEGMENTS",
                                    "originDestinationIds": ["2"],
                                }
                            ]
                            if trip_type == "roundtrip"
                            else []
                        ),
                    ],
                },
            },
        }
    )

    offers = response.data

    def minutes(duration: str):
        # "PT31H30M"
        s = duration.replace("PT", "")
        h = int(s.split("H")[0]) if "H" in s else 0
        m = int(s.split("H")[1].replace("M", "")) if "H" in s and "M" in s else (int(s.replace("M", "")) if "M" in s else 0)
        return h * 60 + m

    filtered = []
    for o in offers:
        ok = True
        for it in o.get("itineraries", []):
            # still filter even with connectionRestriction
            if len(it.get("segments", [])) - 1 > max_connections:
                ok = False
            if max_total_minutes and minutes(it.get("duration", "PT0M")) > max_total_minutes:
                ok = False

        if baggage_included_only:
            ok = any(
                f.get("includedCheckedBags", {}).get("quantity", 0) > 0
                for tp in o.get("travelerPricings", [])
                for f in tp.get("fareDetailsBySegment", [])
            )

        if ok:
            filtered.append(o)

    filtered.sort(key=lambda o: float(o["price"]["grandTotal"]))
    
    time.sleep(2)

    return filtered[:max_results]