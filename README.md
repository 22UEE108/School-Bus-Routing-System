# School Bus Routing System

## Overview
This project is a backend-focused school bus routing system that dynamically assigns buses to pickup points (places) based on connectivity and bus capacity. It allows administrators to manage pickup locations, visualize routes, and handle updates efficiently. The system integrates Google Maps API to compute distances between places and supports dynamic updates when new nodes or connections are added.

---

## Purpose
- Optimize school bus routes for maximum efficiency and minimum travel time.
- Dynamically assign buses based on capacity and route coverage.
- Provide a clear API interface for frontend clients to request bus assignments and update the network.
- Designed for single or multiple schools with minimal changes.

---

## Tech Stack
- **Python 3.11+**
- **FastAPI** – Backend API framework
- **SQLAlchemy (async)** – Async ORM for database interactions
- **MySQL / MariaDB** – Relational database for storing places, buses, distances, and assignments
- **Google Maps API** – Distance calculation and route validation
- **Asyncio / Heapq** – Asynchronous operations and priority queue for optimized route assignment

---

## Project Structure
- **db_models.py** – Database models: `Place`, `GraphEdge`, `Bus`, `RouteAssignment`, with async engine setup.
- **bus_routing_backend.py** – Core backend logic:
  - Fetches distances using Google Maps with caching
  - Builds adjacency list
  - Computes connected components using DFS
  - Assigns buses with max-heap strategy
  - Handles dynamic updates for nodes and edges
- **bus_routes_api.py** – FastAPI interface for:
  - Assigning buses (`/assign_buses`)
  - Fetching current assignments (`/bus_assignments`)
  - Updating nodes and edges dynamically
- **frontend_sim.py** – Minimal client simulation:
  - Connects to API endpoints
  - Fetches and prints assignments
  - Simulates node and edge updates

---

## Algorithm & Optimization
1. **Graph Representation**: Pickup points modeled as nodes; connections/roads as edges.
2. **Distance Fetching**:  
   - Google Maps API is called only if distance is not already cached in the database.
   - Reduces API calls and speeds up route computation.
3. **Route Computation**:
   - DFS to identify connected components (routes) in the graph.
   - Components sorted by size.
   - Buses assigned using a max-heap based on capacity.
4. **Dynamic Updates**:
   - Node or edge changes trigger recomputation only for affected routes.
   - Minimizes unnecessary recalculation.
5. **Scalability**:
   - Supports thousands of nodes due to async DB operations and caching.
   - Can extend to multiple schools by adding a `school_id` filter in tables.

---


