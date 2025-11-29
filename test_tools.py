from travel_planner.tools import find_nearby_places

print("Testing find_nearby_places...")
print("-" * 20)
try:
    results = find_nearby_places("restaurants", "New York", limit=3)
    print(results)
except Exception as e:
    print(f"Test failed with error: {e}")
print("-" * 20)
