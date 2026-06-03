import requests

store = 'STORE_BLR_002'
response = requests.get(f'http://localhost:8000/stores/{store}/metrics')
print(f'Status: {response.status_code}')
metrics = response.json()
print(f'\n✅ STORE_BLR_002 Metrics:')
print(f'- Unique Visitors: {metrics.get("unique_visitors")}')
print(f'- Conversion Rate: {metrics.get("conversion_rate")}%')
print(f'- Queue Depth: {metrics.get("queue_depth")}')
print(f'- Abandonment Rate: {metrics.get("abandonment_rate")}%')
print(f'- Most Visited Zone: {metrics.get("most_visited_zone")}')
print(f'- Avg Dwell Time: {metrics.get("avg_dwell_per_zone")}')
