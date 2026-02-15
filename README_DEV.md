`index.html` - main file to modify page content
`templates` - folder containing various dummy html files.
`legal` - folder containing T&C and COC.
`assets` - folder containing images, css, and js


## How to Run locally

### 1. Environment Setup
- Install [uv](https://github.com/astral-sh/uv) if not already installed.
- Create a `.env` file from `.env.example`:
  ```bash
  cp .env.example .env
  ```
- Update `DATABASE_URL` in `.env` (Use local SQLite or Supabase Postgres).

### 2. Initialize Database & Admin
Run this command to create tables and a default admin user:
```powershell
# Windows (PowerShell)
$env:PYTHONPATH=".;src"
uv run python scripts/setup.py
```

### 3. Run the Project
Start the development server:
```powershell
# Windows (PowerShell)
$env:PYTHONPATH=".;src"
uv run python src/app/main.py
```
Open [http://localhost:10000](http://localhost:10000) in your browser.

### 4. Admin Access
- **URL**: `http://localhost:10000/login`
- **Default Email**: `admin@test.com`
- **Default Password**: `secret` (Check `.env` for `ADMIN_PASSWORD`)

---

## Image optimization
```bash
# Install on your local
sudo apt install graphicsmagick-imagemagick-compat

# Convert all team photos
for file in assets/img/team/*.png; do
    convert "$file" -resize 300x300^ -gravity center -extent 300x300 -quality 80 "${file%.*}.jpg" && rm "$file"
done

# Convert all activity images
for file in assets/img/activities/*.png; do
    convert "$file" -quality 80 -resize 800x600 "${file%.*}.jpg" && rm "$file"
done

# convert a specific photo
img=assets/img/activities/3rd_mlsat.jpg
convert "$img" -quality 80 -resize 800x600 "$img"

convert "$img" -quality 80 -resize 800x600 "${img%.*}.jpg" && rm "$img"
```

### resource
we can this doc for GitHub Page DNS management: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site?platform=linux