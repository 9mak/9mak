import requests
import os
import re

def get_repo_languages(username):
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos = requests.get(repos_url, headers=headers).json()
    
    languages = set()
    for repo in repos:
        lang = repo['language']
        if lang:
            languages.add(lang.lower())
    
    return languages

def update_readme(languages):
    language_to_icon = {
        'ableton': 'ableton', 'activitypub': 'activitypub', 'actix': 'actix', 'adonis': 'adonis',
        'ae': 'ae', 'aiscript': 'aiscript', 'alpinejs': 'alpinejs', 'anaconda': 'anaconda',
        'androidstudio': 'androidstudio', 'angular': 'angular', 'ansible': 'ansible',
        'apollo': 'apollo', 'apple': 'apple', 'appwrite': 'appwrite', 'arch': 'arch',
        'arduino': 'arduino', 'astro': 'astro', 'atom': 'atom', 'au': 'au', 'autocad': 'autocad',
        'aws': 'aws', 'azul': 'azul', 'azure': 'azure', 'babel': 'babel', 'bash': 'bash',
        'bevy': 'bevy', 'bitbucket': 'bitbucket', 'blender': 'blender', 'bootstrap': 'bootstrap',
        'bsd': 'bsd', 'bun': 'bun', 'c': 'c', 'csharp': 'cs', 'cpp': 'cpp', 'crystal': 'crystal',
        'cassandra': 'cassandra', 'clion': 'clion', 'clojure': 'clojure', 'cloudflare': 'cloudflare',
        'cmake': 'cmake', 'codepen': 'codepen', 'coffeescript': 'coffeescript', 'css': 'css',
        'cypress': 'cypress', 'd3': 'd3', 'dart': 'dart', 'debian': 'debian', 'deno': 'deno',
        'devto': 'devto', 'discord': 'discord', 'discordbots': 'bots', 'discordjs': 'discordjs',
        'django': 'django', 'docker': 'docker', 'dotnet': 'dotnet', 'dynamodb': 'dynamodb',
        'eclipse': 'eclipse', 'elasticsearch': 'elasticsearch', 'electron': 'electron',
        'elixir': 'elixir', 'elysia': 'elysia', 'emacs': 'emacs', 'ember': 'ember',
        'emotion': 'emotion', 'express': 'express', 'fastapi': 'fastapi', 'fediverse': 'fediverse',
        'figma': 'figma', 'firebase': 'firebase', 'flask': 'flask', 'flutter': 'flutter',
        'forth': 'forth', 'fortran': 'fortran', 'gamemakerstudio': 'gamemakerstudio',
        'gatsby': 'gatsby', 'gcp': 'gcp', 'git': 'git', 'github': 'github',
        'githubactions': 'githubactions', 'gitlab': 'gitlab', 'gmail': 'gmail', 'gherkin': 'gherkin',
        'go': 'go', 'gradle': 'gradle', 'godot': 'godot', 'grafana': 'grafana', 'graphql': 'graphql',
        'gtk': 'gtk', 'gulp': 'gulp', 'haskell': 'haskell', 'haxe': 'haxe', 'haxeflixel': 'haxeflixel',
        'heroku': 'heroku', 'hibernate': 'hibernate', 'html': 'html', 'htmx': 'htmx', 'idea': 'idea',
        'ai': 'ai', 'instagram': 'instagram', 'ipfs': 'ipfs', 'java': 'java', 'javascript': 'js',
        'jenkins': 'jenkins', 'jest': 'jest', 'jquery': 'jquery', 'kafka': 'kafka', 'kali': 'kali',
        'kotlin': 'kotlin', 'ktor': 'ktor', 'kubernetes': 'kubernetes', 'laravel': 'laravel',
        'latex': 'latex', 'less': 'less', 'linkedin': 'linkedin', 'linux': 'linux', 'lit': 'lit',
        'lua': 'lua', 'markdown': 'md', 'mastodon': 'mastodon', 'materialui': 'materialui',
        'matlab': 'matlab', 'maven': 'maven', 'mint': 'mint', 'misskey': 'misskey',
        'mongodb': 'mongodb', 'mysql': 'mysql', 'neovim': 'neovim', 'nestjs': 'nestjs',
        'netlify': 'netlify', 'nextjs': 'nextjs', 'nginx': 'nginx', 'nim': 'nim', 'nix': 'nix',
        'nodejs': 'nodejs', 'notion': 'notion', 'npm': 'npm', 'nuxtjs': 'nuxtjs', 'obsidian': 'obsidian',
        'ocaml': 'ocaml', 'octave': 'octave', 'opencv': 'opencv', 'openshift': 'openshift',
        'openstack': 'openstack', 'p5js': 'p5js', 'perl': 'perl', 'photoshop': 'ps', 'php': 'php',
        'phpstorm': 'phpstorm', 'pinia': 'pinia', 'pkl': 'pkl', 'plan9': 'plan9',
        'planetscale': 'planetscale', 'pnpm': 'pnpm', 'postgres': 'postgres', 'postman': 'postman',
        'powershell': 'powershell', 'premiere': 'pr', 'prisma': 'prisma', 'processing': 'processing',
        'prometheus': 'prometheus', 'pug': 'pug', 'pycharm': 'pycharm', 'python': 'py',
        'pytorch': 'pytorch', 'qt': 'qt', 'r': 'r', 'rabbitmq': 'rabbitmq', 'rails': 'rails',
        'raspberrypi': 'raspberrypi', 'react': 'react', 'reactivex': 'reactivex', 'redhat': 'redhat',
        'redis': 'redis', 'redux': 'redux', 'regex': 'regex', 'remix': 'remix', 'replit': 'replit',
        'rider': 'rider', 'robloxstudio': 'robloxstudio', 'rocket': 'rocket', 'rollupjs': 'rollupjs',
        'ros': 'ros', 'ruby': 'ruby', 'rust': 'rust', 'sass': 'sass', 'spring': 'spring',
        'sqlite': 'sqlite', 'stackoverflow': 'stackoverflow', 'styledcomponents': 'styledcomponents',
        'sublime': 'sublime', 'supabase': 'supabase', 'scala': 'scala', 'sklearn': 'sklearn',
        'selenium': 'selenium', 'sentry': 'sentry', 'sequelize': 'sequelize', 'sketchup': 'sketchup',
        'solidity': 'solidity', 'solidjs': 'solidjs', 'svelte': 'svelte', 'svg': 'svg',
        'swift': 'swift', 'symfony': 'symfony', 'tailwind': 'tailwind', 'tauri': 'tauri',
        'tensorflow': 'tensorflow', 'terraform': 'terraform', 'threejs': 'threejs', 'twitter': 'twitter',
        'typescript': 'ts', 'ubuntu': 'ubuntu', 'unity': 'unity', 'unreal': 'unreal', 'v': 'v',
        'vala': 'vala', 'vercel': 'vercel', 'vim': 'vim', 'visualstudio': 'visualstudio',
        'vite': 'vite', 'vitest': 'vitest', 'vscode': 'vscode', 'vscodium': 'vscodium',
        'vue': 'vue', 'vuetify': 'vuetify', 'wasm': 'wasm', 'webflow': 'webflow', 'webpack': 'webpack',
        'webstorm': 'webstorm', 'windicss': 'windicss', 'windows': 'windows', 'wordpress': 'wordpress',
        'workers': 'workers', 'xd': 'xd', 'yarn': 'yarn', 'yew': 'yew', 'zig': 'zig'
    }
    
    icons = ','.join([language_to_icon.get(lang, lang) for lang in languages if lang in language_to_icon])
    
    with open('README.md', 'r') as file:
        content = file.read()
    
    skills_line = f'<p align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i={icons}&perline=6" /></a></p>'
    
    # READMEの該当部分を更新
    pattern = r'<p align="center">.*?<\/p>'
    updated_content = re.sub(pattern, skills_line, content, flags=re.DOTALL)
    
    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == '__main__':
    username = '9mak'  # GitHubのユーザー名を指定
    languages = get_repo_languages(username)
    update_readme(languages)