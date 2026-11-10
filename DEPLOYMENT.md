# 🚀 ESTATIQ — Production Deployment Guide
## Complete Walkthrough for GitHub, Render (FastAPI), and Vercel (Next.js)

This step-by-step guide walks you through deploying the **ESTATIQ** platform to production:
- **Backend API & ML Pipeline:** Hosted on **Render** (Python FastAPI)
- **Frontend SaaS Dashboard:** Hosted on **Vercel** (Next.js 14)
- **Source Control:** Hosted on **GitHub**

---

## 📋 Pre-Deployment Architecture

```
                       ┌─────────────────────────────┐
                       │     GitHub Repository       │
                       │ (Source Code & Model .pkl)  │
                       └──────────────┬──────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
┌───────────────────────────┐                   ┌───────────────────────────┐
│     Render (Backend)      │                   │     Vercel (Frontend)     │
│   Python 3.11 + FastAPI   │                   │      Next.js 14 App       │
│ • Root Dir: backend       │ ◄── HTTPS API ─── │ • Root Dir: frontend      │
│ • Serves ML Model (.pkl)  │     /predict      │ • Client-side UI Form     │
│ • Endpoints: /health,     │                   │ • Env: NEXT_PUBLIC_...    │
│   /model-info, /predict   │                   │                           │
└───────────────────────────┘                   └───────────────────────────┘
```

---

## STEP 1: Push Code to GitHub

Open your terminal in `c:\MY FILES\CODING\ML Project`:

```bash
# 1. Initialize git (already initialized in workspace)
git init

# 2. Add all files (models, frontend, backend, documentation)
git add .

# 3. Create initial commit
git commit -m "feat: complete ESTATIQ full-stack production release"

# 4. Create a new repository on GitHub (e.g., https://github.com/your-username/estatiq-house-price)

# 5. Link your local repo to GitHub and push
git branch -M main
git remote add origin https://github.com/your-username/estatiq-house-price.git
git push -u origin main
```

> **Note on Model Size:** The Random Forest model file `backend/models/house_price_model.pkl` is ~34.5 MB, which is well below GitHub's 100 MB hard file limit. It commits and pushes seamlessly without needing Git LFS.

---

## STEP 2: Deploy Backend to Render (FastAPI)

1. Sign up or log in at **[render.com](https://render.com)**.
2. From the dashboard, click **"New +"** and select **"Web Service"**.
3. Connect your GitHub repository (`estatiq-house-price`).
4. Configure the Web Service settings:
   - **Name:** `estatiq-backend` (or your preferred name)
   - **Region:** Any close region (e.g., `Singapore` or `Frankfurt` or `Oregon`)
   - **Branch:** `main`
   - **Root Directory:** `backend` ⚠️ *(Crucial)*
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
5. Expand **Advanced Settings**:
   - Add Environment Variable:
     - Key: `PYTHON_VERSION`
     - Value: `3.11.9`
   - **Health Check Path:** `/health`
6. Click **"Create Web Service"**.
7. Wait 2–3 minutes for the build to finish. Once live, Render will provide your public backend URL, e.g.:
   ```
   https://estatiq-backend.onrender.com
   ```
8. **Verify the Backend:**
   Open in your browser:
   - `https://estatiq-backend.onrender.com/health` ➔ Should return `{"status": "healthy", "model_loaded": true}`
   - `https://estatiq-backend.onrender.com/docs` ➔ Interactive Swagger UI documentation

---

## STEP 3: Deploy Frontend to Vercel (Next.js)

1. Sign up or log in at **[vercel.com](https://vercel.com)**.
2. Click **"Add New..."** ➔ **"Project"**.
3. Import your GitHub repository (`estatiq-house-price`).
4. In the **Configure Project** screen:
   - **Project Name:** `estatiq`
   - **Framework Preset:** `Next.js`
   - **Root Directory:** Click "Edit" and choose `frontend` ⚠️ *(Crucial)*
5. Expand **Environment Variables**:
   - **Name:** `NEXT_PUBLIC_API_BASE_URL`
   - **Value:** `https://estatiq-backend.onrender.com` *(Paste your Render backend URL from Step 2, without a trailing slash)*
6. Click **"Deploy"**.
7. Vercel will build the Next.js application in ~45 seconds and provide your live production domain:
   ```
   https://estatiq.vercel.app
   ```

---

## STEP 4: Live Verification & Testing

Once both services are deployed:
1. Open your Vercel URL: `https://estatiq.vercel.app`.
2. Notice the top-right status pill in the navbar:
   - It will ping `https://estatiq-backend.onrender.com/health` and display a glowing green dot: **"ML Engine Online"**.
3. Scroll to the **Valuation Studio** form.
4. Select property specifications (e.g., 2 BHK Apartment in Andheri West, Mumbai, 1100 sq.ft.).
5. Click **"CALCULATE ESTIMATED PROPERTY VALUE"**.
6. The gold result card will render the exact valuation calculated live by your Scikit-learn model on Render.

---

## 🛠️ Local Development Quickstart

If you wish to run both frontend and backend locally on your computer:

### Terminal 1: Run FastAPI Backend
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*API will run at `http://127.0.0.1:8000` (docs at `http://127.0.0.1:8000/docs`).*

### Terminal 2: Run Next.js Frontend
```bash
cd frontend
npm run dev
```
*Frontend will run at `http://localhost:3000`.*

