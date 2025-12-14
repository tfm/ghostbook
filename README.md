# Ghostbook

Ghostbook provides automation tools to turn your Facebook account into a shell account, if you still need an account but want minimal personal information on it.

I'm sharing it hoping it's useful to others, since Facebook doesn't provide any way to bulk remove friends or set the visibility on existing content, but it was written very quickly with the assistance of Gemini and not built to be robust or expecting to survive any changes in the Facebook UI.

## Tools

### Friend Remover (`delete_friends.py`)
This script automates the process of removing friends from your Facebook account.

**Usage:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python delete_friends.py
   ```
3. Follow the on-screen prompts:
   - Log in to Facebook in the browser window that opens.
   - Navigate to your profile -> Friends -> **All Friends**.
   - Press Enter in the terminal to start the deletion process.

### Photo Hider (`hide_photos.py`)
This script automates the process of changing the privacy of your photos to "Only me".

**Usage:**
1. Install dependencies (if not already done):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python hide_photos.py
   ```
3. Follow the on-screen prompts:
   - Log in to Facebook in the browser window that opens.
   - Navigate to your **Profile** -> **Photos** -> **Your Photos**.
   - **Click on the first photo** to open it in full screen (theater mode).
   - Press Enter in the terminal to start the process.

**⚠️ Important Notes:**
- **Experimental:** These scripts are experimental and may contain bugs.
- **Multiple Runs:** You may need to run the deletion script multiple times to successfully remove all friends. The script might stop or fail due to Facebook UI changes.

## License
MIT
