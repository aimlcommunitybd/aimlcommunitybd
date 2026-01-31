# AI/ML Professional Community Bangladesh

This repo contains our community website sourcecode. The Site is build on the following stack:
1. Frontend: HTML/CSS, JS
2. Backend: Python, Flask
3. Database: SQLite
4. Infrastructure: Render Webserver Instance
5. Version Control: git & github.
6. Dependency Management: uv-astral

## Quick Setup

Before setup, you'll need Python, git and UV in your system.
- Python installatin doc: https://www.python.org/downloads/
- Git install doc: https://git-scm.com/install/
- uv-astral installation doc: https://docs.astral.sh/uv/getting-started/installation/

```bash
git clone https://github.com/aimlcommunitybd/aimlcommunitybd.git
cd aimlcommunitybd
cp .env.example .env

uv sync
source .venv/bin/activate
make dev # setup new db
make server
```

By default, you'll find the webapp is running on `http://0.0.0.0:10000/`.


## How to contribute
1. Clone the repository to your local
2. Create a new branch using `git checkout -b <branch-name>
3. Develop or Fix on your new branch, commit your changes and push. 
4. Then submit a Pull Request with detailed description
