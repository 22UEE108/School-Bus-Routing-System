import requests

API_BASE = "http://127.0.0.1:8000"

# # Compute and assign buses
resp = requests.post(f"{API_BASE}/assign_buses")
if resp.status_code == 200:
    print("Assignments after computation:")
    for a in resp.json().get("assignments", []):
        print(f"Bus {a['bus_id']} -> {a['route']}")
else:
    print("Error:", resp.text)

# # Fetch current assignments
resp = requests.get(f"{API_BASE}/bus_assignments")
if resp.status_code == 200:
    print("\nCurrent assignments from DB:")
    for a in resp.json().get("assignments", []):
        print(f"Bus {a['bus_id']} -> {a['route']}")
else:
    print("Error:", resp.text)

# # Update node example (add/remove place)
update_node_payload = {"place_id": 5, "action": "remove"}  # just example
resp = requests.post(f"{API_BASE}/update_node", json=update_node_payload)
if resp.status_code == 200:
    print("\nAssignments after node update:")
    for a in resp.json().get("assignments", []):
        print(f"Bus {a['bus_id']} -> {a['route']}")
else:
    print("Error:", resp.text)

# # Update edge example (add/remove connection)
update_edge_payload = {"from_id": 1, "to_id": 2, "action": "add"}  # just example
resp = requests.post(f"{API_BASE}/update_edge", json=update_edge_payload)
if resp.status_code == 200:
    print("\nAssignments after edge update:")
    for a in resp.json().get("assignments", []):
        print(f"Bus {a['bus_id']} -> {a['route']}")
else:
    print("Error:", resp.text)
