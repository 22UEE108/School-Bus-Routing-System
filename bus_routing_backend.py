import asyncio
import heapq
from typing import List, Dict, Set, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from db_models import AsyncSessionLocal, Place, PlaceDistance, Bus, RouteAssignment, Base, engine
import googlemaps

# -----------------------------
# GOOGLE MAPS CLIENT
# -----------------------------
GMAPS_API_KEY = "YOUR_API_KEY"
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
async def fetch_distance(session: AsyncSession, from_id: int, to_id: int) -> float:
    """Fetch distance between two places using cache/db or Google Maps API."""
    if from_id == to_id:
        return 0.0

    # Check in DB first
    result = await session.execute(
        "SELECT distance FROM place_distances WHERE (from_place_id=:f AND to_place_id=:t) OR (from_place_id=:t AND to_place_id=:f)",
        {"f": from_id, "t": to_id}
    )
    row = result.scalar_one_or_none()
    if row is not None:
        return float(row)

    # Fetch from Google Maps
    result = await session.execute(
        "SELECT name FROM places WHERE place_id=:id", {"id": from_id}
    )
    from_name = result.scalar_one()
    result = await session.execute(
        "SELECT name FROM places WHERE place_id=:id", {"id": to_id}
    )
    to_name = result.scalar_one()

    distance_matrix = gmaps.distance_matrix(from_name, to_name)
    dist = distance_matrix['rows'][0]['elements'][0]['distance']['value']  # in meters

    # Save to DB
    await session.execute(
        "INSERT INTO place_distances (from_place_id, to_place_id, distance) VALUES (:f,:t,:d)",
        {"f": from_id, "t": to_id, "d": dist}
    )
    await session.commit()
    return dist

async def build_adjacency(session: AsyncSession) -> Dict[int, Set[int]]:
    """Build adjacency list based on available distances."""
    result = await session.execute("SELECT place_id FROM places")
    place_ids = [row[0] for row in result.all()]
    adj = {pid: set() for pid in place_ids}

    # Connect nodes that have distance in DB or API (here we fully connect all for simplicity)
    for i, u in enumerate(place_ids):
        for v in place_ids[i+1:]:
            dist = await fetch_distance(session, u, v)
            if dist > 0:
                adj[u].add(v)
                adj[v].add(u)
    return adj

def dfs(node: int, adj: Dict[int, Set[int]], visited: Set[int]) -> List[int]:
    """DFS to get connected component"""
    stack = [node]
    comp = []
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            comp.append(curr)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    stack.append(neighbor)
    return comp

# -----------------------------
# ROUTE COMPUTATION
# -----------------------------
async def compute_routes(session: AsyncSession) -> List[Dict]:
    """Compute bus assignments"""
    bus_result = await session.execute("SELECT bus_id, capacity FROM buses ORDER BY capacity DESC")
    buses = [(row.capacity, row.bus_id) for row in bus_result.all()]
    heapq._heapify_max(buses)

    adj = await build_adjacency(session)

    visited = set()
    components = []
    for pid in adj:
        if pid not in visited:
            comp = dfs(pid, adj, visited)
            components.append(comp)
    components.sort(key=lambda x: len(x), reverse=True)

    assignments = []
    for comp in components:
        if not buses:
            break
        cap, bus_id = heapq._heappop(buses)
        assignments.append({"bus_id": bus_id, "route": comp})
        # Save assignment
        session.add(RouteAssignment(bus_id=bus_id, places=comp))
    await session.commit()
    return assignments
