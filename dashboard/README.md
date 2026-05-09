# MWIT #14 — Ticket Sales Dashboard

A shareable, public dashboard built from `MWIT14_tracker.xlsx`.

## What's in this folder

| File | What it does |
| --- | --- |
| `index.html` | The dashboard. Loads `data.json` on open. |
| `data.json` | Numbers extracted from the Excel file. |
| `refresh.py` | Re-reads the Excel file and rewrites `data.json`. |
| `README.md` | This file. |

## Daily refresh — 30 seconds

1. Update `MWIT14_tracker.xlsx` like you normally would (overwrite the file in the same place).
2. From this `dashboard/` folder, run:

   ```bash
   python3 refresh.py
   ```

   This rewrites `data.json` with the new totals.

3. Push the change to whichever host you're using (see below).

> First-time setup: `pip install openpyxl --break-system-packages` (or use a virtualenv).

## Deployment options

You only need to do this once. After that, daily updates are just step 1–3 above.

### Option A — Netlify Drop (fastest, no account, ~1 min)

1. Go to <https://app.netlify.com/drop>.
2. Drag this entire `dashboard/` folder onto the page.
3. Netlify gives you a public URL like `https://kind-fox-1234.netlify.app`. Share that.
4. **For daily updates:** drag the folder again to the same site (Netlify lets you redeploy by drag-and-drop on the site overview page) — the URL stays the same.

If you want to keep the URL stable across drops, sign in (free) and use *Sites → Deploys → Drag-and-drop* on the existing site.

### Option B — GitHub Pages (free, version-controlled)

1. Create a public repo on GitHub, e.g. `mwit14-dashboard`.
2. From your machine:

   ```bash
   cd "/Users/peanutzhou/AI/Claude/MWIT/dashboard"
   git init
   git add .
   git commit -m "Initial dashboard"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USER>/mwit14-dashboard.git
   git push -u origin main
   ```

3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `/ (root)` → Save.**
4. After ~1 minute, your dashboard is live at:
   `https://<YOUR_USER>.github.io/mwit14-dashboard/`

5. **For daily updates:**

   ```bash
   python3 refresh.py
   git commit -am "Refresh data $(date +%Y-%m-%d)"
   git push
   ```

   GitHub Pages updates automatically within a minute.

### Option C — Any static host (Cloudflare Pages, Vercel, Render, S3, etc.)

The folder is a plain static site. Drop it anywhere that serves HTML.

## Local preview

`index.html` uses `fetch()` to load `data.json`, which most browsers block when opened directly via `file://`. To preview before deploying, run a quick local server:

```bash
cd "/Users/peanutzhou/AI/Claude/MWIT/dashboard"
python3 -m http.server 8000
# then open http://localhost:8000
```

## Customizing

- **Sales target** comes from the Excel cell labelled `Sales Target:`. Change it in the spreadsheet and rerun `refresh.py`.
- **Colors / layout** are in `index.html` (CSS variables at the top of `<style>`).
- **More charts / fields** — extend the JSON in `refresh.py` and read it in `index.html`.
