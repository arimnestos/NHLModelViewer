# NHL Model Viewer

A Streamlit app to view key NHL model data on any device.

## Features
- Shows games for today and tomorrow
- Displays key columns: Team, H/A, Starting Goalie, ADJ TO FAIR, Confidence, Model Fair Values
- Auto-refreshes with a "Reload Data" button
- Mobile-friendly interface

## Local Setup

Run the app locally:
```bash
streamlit run app.py
```

## Deploying to Streamlit Cloud

### Prerequisites
1. GitHub account
2. The Excel file needs to be accessible to the Streamlit Cloud app

### Steps

1. **Create a GitHub Repository**
   - Go to https://github.com/new
   - Name it something like `nhl-model-viewer`
   - Make it private (recommended since it contains your model data)
   - Don't initialize with README (we already have files)

2. **Push Your Code to GitHub**
   
   Open Terminal and navigate to this folder:
   ```bash
   cd "/Users/alexanderracher/Library/CloudStorage/GoogleDrive-alexander.racher@gmail.com/My Drive/NHL 2025-26/Model Viewer App"
   ```
   
   Initialize git and push:
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit - NHL Model Viewer"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/nhl-model-viewer.git
   git push -u origin main
   ```
   (Replace `YOUR_USERNAME` with your GitHub username)

3. **Upload Excel File to GitHub**
   
   Since the Excel file is in your Dropbox, you have two options:
   
   **Option A: Include it in the repository (simpler)**
   ```bash
   cp "/Users/alexanderracher/Dropbox/nhl/NHL Model 2025.xlsx" .
   git add "NHL Model 2025.xlsx"
   git commit -m "Add model data"
   git push
   ```
   Then update line 15 in app.py to:
   ```python
   FILE_PATH = 'NHL Model 2025.xlsx'
   ```
   
   **Option B: Keep it in Dropbox and use a shared link (requires updating the file path logic)**

4. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/nhl-model-viewer`
   - Main file path: `app.py`
   - Click "Deploy"

5. **Access Your App**
   - Once deployed, you'll get a URL like `https://YOUR_USERNAME-nhl-model-viewer.streamlit.app`
   - You can access this from any device, including your phone!

## Updating the Model

If you choose Option A and want to update the Excel file:
```bash
cd "/Users/alexanderracher/Library/CloudStorage/GoogleDrive-alexander.racher@gmail.com/My Drive/NHL 2025-26/Model Viewer App"
cp "/Users/alexanderracher/Dropbox/nhl/NHL Model 2025.xlsx" .
git add "NHL Model 2025.xlsx"
git commit -m "Update model data"
git push
```

The app will automatically redeploy with the new data.
