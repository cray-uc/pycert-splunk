import requests
import json
from datetime import datetime, timedelta

def send_to_splunk(data, splunk_url, splunk_token):
    headers = {
        'Authorization': f'Splunk {splunk_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(splunk_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error sending data to Splunk: {response.status_code} - {response.text}")

url = "[url_here]"
splunk_url = "https://your-splunk-instance.com:8088/services/collector/event"
splunk_token = "YOUR_SPLUNK_TOKEN"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    current_date = datetime.now()
    thirty_days_ago = current_date - timedelta(days=30)

    domain_check_results = []

    for entry in data:
        common_name = entry.get('common_name')
        entry_timestamp_str = entry.get('entry_timestamp')

        if common_name and entry_timestamp_str:
            entry_timestamp = datetime.fromisoformat(entry_timestamp_str.replace('T', ' '))

            if entry_timestamp >= thirty_days_ago:
                domain_info = {
                    'common_name': common_name,
                    'entry_timestamp': entry_timestamp.isoformat()
                }
                domain_check_results.append(domain_info)

    with open('domain_check_results.json', 'w') as json_file:
        json.dump(domain_check_results, json_file, indent=4)

    # Send data to Splunk
    send_to_splunk(domain_check_results, splunk_url, splunk_token)

else:
    print(f"Error: {response.status_code} - {response.text}")
