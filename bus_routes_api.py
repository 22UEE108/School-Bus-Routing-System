from fastapi import FastAPI, HTTPException
import asyncio
from bus_routing_backend import compute_routes, AsyncSessionLocal, RouteAssignment

app = FastAPI(title="School Bus Routing API")

@app.post("/assign_buses")
async def assign_buses():
    """Compute and assign buses"""
    async with AsyncSessionLocal() as session:
        try:
            assignments = await compute_routes(session)
            return {"status": "success", "assignments": assignments}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/bus_assignments")
async def bus_assignments():
    """Fetch current assignments"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute("SELECT bus_id, places FROM route_assignments")
            data = [{"bus_id": row[0], "route": row[1]} for row in result.all()]
            return {"status": "success", "assignments": data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
