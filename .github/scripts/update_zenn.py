import feedparser
import re
import os

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
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()

        zenn_section = ''
        for post in posts:
            zenn_section += f"- [{post['title']}]({post['link']})\n"

        pattern = r'(## <img src="https://zenn\.dev/images/logo-transparent\.png".*?\n<!-- This section is automatically updated by GitHub Actions -->\n)([\s\S]*?)(?=\n##|\Z)'
        updated_content = re.sub(pattern, r'\1' + zenn_section, content, flags=re.DOTALL)

        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print("README.md has been successfully updated with the latest Zenn articles.")
    except FileNotFoundError:
        print("Error: README.md file not found.")
    except Exception as e:
        print(f"An error occurred while updating README: {e}")

if __name__ == '__main__':
    try:
        username = os.environ.get('GITHUB_USERNAME', '9mak')
        feed_url = f"https://zenn.dev/{username}/feed"
        latest_posts = get_latest_zenn_posts(feed_url)
        if latest_posts:
            update_readme(latest_posts)
        else:
            print("No Zenn articles found or error occurred while fetching articles.")
    except Exception as e:
        print(f"Script execution failed: {e}")