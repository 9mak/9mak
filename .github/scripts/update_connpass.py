import requests
import re
from datetime import datetime

def get_recent_events(nickname, count=3):
    url = f"https://connpass.com/api/v1/event/?nickname={nickname}&order=2&count={count}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['events']
    return []

def format_event(event):
    start_date = datetime.fromisoformat(event['started_at'].replace('Z', '+00:00'))
    return f"- {start_date.strftime('%Y-%m-%d')} [{event['title']}]({event['event_url']})"

def update_readme(events):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    connpass_section = "## Recent Connpass Events\n\n"
    for event in events:
        connpass_section += format_event(event) + "\n"

    pattern = r'## Recent Connpass Events\n\n[\s\S]*?(?=\n##|$)'
    updated_content = re.sub(pattern, connpass_section, content, flags=re.DOTALL)

    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == '__main__':
    nickname = '9mak'  # あなたのconnpassのニックネームに変更してください
    recent_events = get_recent_events(nickname)
    update_readme(recent_events)