# GitHub Auto-Update Setup Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - Name: `MochiPet`
   - Description: "Desktop pet water reminder"
   - Make it **Public** (important for updates to work)
   - Click "Create repository"

## Step 2: Update the Code

In `updater.py`, find this line:
```python
GITHUB_REPO = "YOUR_USERNAME/MochiPet"
```

Replace `YOUR_USERNAME` with your actual GitHub username.

Example:
```python
GITHUB_REPO = "yogit/MochiPet"
```

## Step 3: Initial Setup

1. Run `build.bat` to rebuild the installer
2. Go to your GitHub repo
3. Click "Releases" (right side)
4. Click "Create a new release"
5. **Tag version:** `1.0`
6. **Title:** `MochiPet v1.0 - Initial Release`
7. Upload file: `dist/MochiPet.exe` (NOT the Setup.exe, just the exe)
8. Click "Publish release"

## Step 4: Share with Users

- Share the **installer**: `installer/MochiPet-Setup.exe`
- Users install it once
- App will auto-update from GitHub releases

## Step 5: Future Updates

Each time you update:

1. Make code changes
2. Run `build.bat` locally
3. Go to GitHub → Releases → "Create a new release"
4. **Tag version:** `1.1` (increment the number)
5. **Title:** `MochiPet v1.1 - New Features`
6. Upload: `dist/MochiPet.exe` 
7. Click "Publish release"

**That's it!** Users' apps will auto-update automatically! ✨

---

## Troubleshooting

- **Updates not working?** Make sure repo is **PUBLIC**, not private
- **Version not recognized?** Make sure tag is formatted as version (e.g., `1.0`, `1.1`, `2.0`)
- **Still not working?** Check that `GITHUB_REPO` in updater.py matches your username/repo exactly
