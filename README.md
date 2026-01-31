# AI/ML Professional Community Bangladesh

This repo contains our community website sourcecode. 

The official website for the AI/ML Professional Community Bangladesh, a vibrant community of AI and ML enthusiasts, professionals, and learners in Bangladesh.


## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python 3.12, Flask |
| **Database** | SQLite |
| **Deployment** | Render |
| **Package Manager** | uv (Astral) |
| **Version Control** | Git & GitHub |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **Git** - [Install Guide](https://git-scm.com/install/)
- **uv** - [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)


## Quick Setup

```bash
git clone https://github.com/aimlcommunitybd/aimlcommunitybd.git
cd aimlcommunitybd
cp .env.example .env

uv sync
source .venv/bin/activate
make dev # setup new db
make server
```

Visit [http://0.0.0.0:10000](http://0.0.0.0:10000) in your browser to see the application running.


## 📂 Project Structure

```
aimlcommunitybd/
├── src/
│   └── app/
│       ├── assets/          # Static files (CSS, JS, images)
│       ├── templates/       # HTML templates
│       ├── models.py        # Database models
│       ├── main.py          # Flask application
│       ├── db.py            # Database configuration
│       ├── settings.py      # Application settings
│       └── utils.py         # Utility functions
├── scripts/
│   ├── populate_activities.py  # Seed activities data
│   ├── populate_admin.py       # Create admin user
│   └── setup.py                # Setup script
├── Makefile                 # Build automation
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```


## 🤝 Contributing

1. Clone the repo to your local (or Fork the repo first then clone) 
2. Create a new branch using `git checkout -b <branch-name>`  
3. Develop or Fix on your new branch, commit your changes and push.   
4. Then submit a Pull Request with detailed description  


### Contribution Guidelines

- Follow PEP 8 style guide for Python code  
- Write meaningful commit messages  
- Update documentation if needed  
- Ensure all tests pass before submitting PR  
- Be respectful and constructive in discussions  

## 🐛 Bug Reports

Found a bug? Please open an issue with:  
- Clear description of the problem  
- Steps to reproduce  
- Expected vs actual behavior  
- Screenshots if applicable  
 

---

Made with ❤️ by the AI/ML Professional Community Bangladesh