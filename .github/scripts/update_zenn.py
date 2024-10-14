import feedparser
import re

def get_latest_zenn_posts(feed_url, num_posts=5):
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries[:num_posts]:
        posts.append({
            'title': entry.title,
            'link': entry.link
        })
    return posts

def update_readme(posts):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    zenn_section = "## Latest Zenn Articles\n\n"
    for post in posts:
        zenn_section += f"- [{post['title']}]({post['link']})\n"

    pattern = r'## Latest Zenn Articles\n\n[\s\S]*?(?=\n##|$)'
    updated_content = re.sub(pattern, zenn_section, content, flags=re.DOTALL)

    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == '__main__':
    feed_url = "https://zenn.dev/9mak/feed"
    latest_posts = get_latest_zenn_posts(feed_url)
    update_readme(latest_posts)