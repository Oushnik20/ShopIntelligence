import requests

store = 'STORE_BLR_002'

print('Testing API endpoints...\n')

# Test Funnel
funnel_response = requests.get(f'http://localhost:8000/stores/{store}/funnel')
print(f'Funnel Status: {funnel_response.status_code}')
funnel = funnel_response.json()
print(f'Funnel Data: {funnel}\n')

# Test Anomalies
anomalies_response = requests.get(f'http://localhost:8000/stores/{store}/anomalies')
print(f'Anomalies Status: {anomalies_response.status_code}')
anomalies = anomalies_response.json()
print(f'Anomalies Data: {anomalies}\n')

# Test Metrics
metrics_response = requests.get(f'http://localhost:8000/stores/{store}/metrics')
print(f'Metrics Status: {metrics_response.status_code}')
metrics = metrics_response.json()
print(f'Dwell Data: {metrics.get("avg_dwell_per_zone")}\n')
