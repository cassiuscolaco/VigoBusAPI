"""CACHE DATA SOURCE
Cached local storages with TTL for Stops and Buses
"""

# # Native # #
from typing import Optional

# # Installed # #
from cachetools import TTLCache
from pybusent import BusesResult

# # Project # #
from vigobusapi.settings_handler import settings

# # Parent Package # #
from ..entities import Stop

__all__ = ("stops_cache", "buses_cache", "save_stop", "save_buses", "get_stop", "get_buses")

stops_cache = TTLCache(maxsize=settings.stops_cache_maxsize, ttl=settings.stops_cache_ttl)
"""Stops Cache. Key: Stop ID. Value: Stop object."""

buses_cache = TTLCache(maxsize=settings.buses_cache_maxsize, ttl=settings.buses_cache_ttl)
"""Buses Cache. Key: tuple (Stop ID, bool GetAllBuses?). Value: BusesResult"""


def save_stop(stop: Stop):
    """This function must be executed whenever a Stop is found by any getter, other than the Stops Cache
    """
    stops_cache[stop.stopid] = stop


def save_buses(stopid: int, get_all_buses: bool, buses_result: BusesResult):
    """This function must be executed whenever a List of Buses for a Stop is found by any getter,
    other than the Stops Cache
    """
    buses_cache[(stopid, get_all_buses)] = buses_result


def get_stop(stopid: int) -> Optional[Stop]:
    """Get a Stop from the Stops Cache. If the Stop is not cached, None is returned.
    """
    return stops_cache.get(stopid)


def get_buses(stopid: int, get_all_buses: bool) -> Optional[BusesResult]:
    """Get List of Buses from the Buses Cache, by Stop ID and All Buses wanted (True/False).
    If the list of buses for the given Stop ID is not cached, None is returned.
    """
    buses_result: Optional[BusesResult] = buses_cache.get((stopid, get_all_buses))
    if buses_result is None and not get_all_buses:
        # If NOT All Buses are requested, and a Not All Buses query is not cached, but an All Buses query is cached,
        # return it, since it is still valid - but limit the results
        buses_result = buses_cache.get((stopid, True))
        if buses_result:
            buses_result.buses = buses_result.buses[:settings.buses_normal_limit]
    return buses_result
