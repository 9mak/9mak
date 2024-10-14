import requests
import re
from datetime import datetime
import os

def get_recent_events(nickname, count=3):
    url = f"https://connpass.com/api/v1/event/?nickname={nickname}&order=2&count={count}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['events']
    except requests.RequestException as e:
        print(f"Error fetching Connpass events: {e}")
        return []

def format_event(event):
    start_date = datetime.fromisoformat(event['started_at'].replace('Z', '+00:00'))
    return f"- {start_date.strftime('%Y-%m-%d')} [{event['title']}]({event['event_url']})"

def update_readme(events):
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()

        connpass_section = ""
        for event in events:
            connpass_section += format_event(event) + "\n"

        pattern = r'(## <img src="https://connpass\.com/static/img/api/connpass_logo_3\.png".*?\n<!-- This section is automatically updated by GitHub Actions -->\n)([\s\S]*?)(?=\n##|\Z)'
        updated_content = re.sub(pattern, r'\1' + connpass_section, content, flags=re.DOTALL)

        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print("README.md has been successfully updated with recent Connpass events.")
    except FileNotFoundError:
        print("Error: README.md file not found.")
    except Exception as e:
        print(f"An error occurred while updating README: {e}")

if __name__ == '__main__':
    try:
        nickname = os.environ.get('CONNPASS_NICKNAME', '9mak')
        recent_events = get_recent_events(nickname)
        if recent_events:
            update_readme(recent_events)
        else:
            print("No recent Connpass events found or error occurred while fetching events.")
    except Exception as e:
        print(f"Script execution failed: {e}")