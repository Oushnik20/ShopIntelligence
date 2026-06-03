import requests

print('=== Metrics for Both Stores ===\n')

for store in ['STORE_BLR_001', 'STORE_BLR_002']:
    response = requests.get(f'http://localhost:8000/stores/{store}/metrics')
    metrics = response.json()
    print(f'{store}:')
    print(f'  - Visitors: {metrics.get("unique_visitors")}')
    print(f'  - Conversion: {metrics.get("conversion_rate")}%')
    print(f'  - Queue Depth: {metrics.get("queue_depth")}')
    print(f'  - Most Visited Zone: {metrics.get("most_visited_zone")}')
    print()
