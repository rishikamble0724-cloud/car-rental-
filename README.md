# Car Rental System — Vercel Deployment

Mini project: HTML/JS frontend + Python (Flask) backend, deployable on Vercel.

## Files

| File | Purpose |
|------|---------|
| `public/index.html` | Frontend page (car list, booking form, bookings table) |
| `public/app.js` | Frontend logic — talks to the backend at `/api` |
| `api/index.py` | Python Flask backend (serverless function) |
| `requirements.txt` | Python packages Vercel installs |
| `vercel.json` | Routes `/api/*` to the Python backend, everything else to the frontend |

## How to deploy on Vercel

1. Create a free account at https://vercel.com
2. Install the Vercel CLI: `npm i -g vercel`
3. Open a terminal inside this folder and run:
   ```
   vercel
   ```
   (Answer the questions with the defaults — press Enter.)
4. Vercel prints your live URL, e.g. `https://car-rental-xxxx.vercel.app`

Or without the CLI: push this folder to a GitHub repository, then in Vercel
click **Add New → Project → Import** your repo. No settings need changing.

## Notes

- The SQLite database is stored in `/tmp` on Vercel, so bookings reset when
  the app redeploys or the serverless function goes cold. For a college demo
  this is fine; the car list is re-created automatically.
- The Java Swing frontend (`CarRentalApp.java`) is not part of this web
  deployment — it is a desktop app. If you want to use it with this backend,
  set its `BACKEND_URL` to `https://your-app.vercel.app/api`.
