# Deploying the Backend (Render or Railway)

Either service works the same way; steps below use Render.

1. Push your repo to GitHub.
2. Go to https://render.com → sign in → "New" → "Web Service"
3. Connect your repository.
4. Settings:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as your local `.env`):
   - `GEMINI_API_KEY`
   - `GOOGLE_API_KEY`
   - `DATABASE_URL` (your Supabase connection string)
6. Click "Create Web Service." First deploy takes a few minutes.
7. Once live, Render gives you a URL like `https://your-app.onrender.com`
   — test it by visiting `https://your-app.onrender.com/docs`
8. Copy this URL into your frontend's `NEXT_PUBLIC_API_BASE` environment
   variable on Vercel (see `vercel_notes.md`), then redeploy the frontend.

## Important: run the knowledge ingest script once after deploying
Chroma's data folder (`backend/chroma_data/`) is local to the deployed
instance. After your first deploy, use Render's "Shell" tab (or a
one-off job) to run:
```
python -m retrieval.ingest_knowledge
```
Otherwise the deployed backend's knowledge base will be empty even
though your local one has data.
