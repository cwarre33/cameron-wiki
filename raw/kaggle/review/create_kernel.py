#!/usr/bin/env python3
"""
Hull Tactical — Create Kernel on Kaggle (automated)

This script automates the first-time setup:
1. Login to Kaggle
2. Navigate to competition
3. Create new notebook
4. Upload submission.py content
5. Add dataset as input
6. Save notebook

Usage:
    export KAGGLE_USERNAME=your_kaggle_email
    export KAGGLE_PASSWORD=your_password
    python create_kernel.py

After this completes, run submit_notebook.py to actually submit.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

KAGGLE_BASE = 'https://www.kaggle.com'
COMPETITION = 'hull-tactical-market-prediction'
KERNEL_SLUG = 'hull-tactical-submission'


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--username', default=os.getenv('KAGGLE_USERNAME'))
    p.add_argument('--password', default=os.getenv('KAGGLE_PASSWORD'))
    p.add_argument('--headless', action='store_true', help='run without browser window')
    return p.parse_args()


def login(page, username: str, password: str):
    print("🔐 Logging in to Kaggle...")
    page.goto(f'{KAGGLE_BASE}/account/login', wait_until='networkidle')
    
    # Click "Sign in with Email" to reveal form
    signin_btn = page.get_by_text('Sign in with Email')
    signin_btn.click()
    page.wait_for_selector('input[name="email"]', timeout=8000)
    
    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)
    page.get_by_role('button', name='Sign In').last.click()
    
    page.wait_for_load_state('networkidle', timeout=20000)
    if '/account/login' in page.url:
        page.screenshot(path='/tmp/kaggle_login_fail.png')
        sys.exit("Login failed - check KAGGLE_USERNAME and KAGGLE_PASSWORD")
    print("  ✅ Logged in")


def create_notebook(page):
    """Navigate to competition and create new notebook"""
    print("📓 Navigating to competition...")
    
    # Go to competition code tab
    page.goto(f'{KAGGLE_BASE}/competitions/{COMPETITION}/code', wait_until='networkidle')
    time.sleep(2)
    
    print("  Looking for 'New Notebook' button...")
    new_nb = page.get_by_text('New Notebook')
    if not new_nb.is_visible(timeout=5000):
        # Try alternative selectors
        new_nb = page.locator('a[href*="/code/new"], button:has-text("New Notebook")').first
    
    if new_nb.is_visible(timeout=3000):
        new_nb.click()
        print("  ✅ Creating new notebook...")
    else:
        # Direct URL
        page.goto(f'{KAGGLE_BASE}/code/new', wait_until='networkidle')
        print("  ✅ Navigated to notebook editor")
    
    page.wait_for_load_state('networkidle', timeout=20000)
    time.sleep(3)


def add_dataset(page):
    """Add hull-tactical-model dataset as input"""
    print("📦 Adding dataset...")
    
    # Click "Add Data" button
    add_data = page.get_by_text('Add Data')
    if not add_data.is_visible(timeout=3000):
        add_data = page.locator('button:has-text("Add Data")').first
    
    if add_data.is_visible(timeout=3000):
        add_data.click()
        time.sleep(2)
        
        # Search for our dataset
        search = page.locator('input[placeholder*="Search"], input[type="search"]').first
        if search.is_visible(timeout=3000):
            search.fill('hull-tactical-model')
            time.sleep(2)
            
            # Click on result
            result = page.get_by_text('hull-tactical-model', exact=False)
            if result.is_visible(timeout=5000):
                result.first.click()
                time.sleep(1)
                
                # Add button
                add_btn = page.get_by_text('Add')
                if add_btn.is_visible(timeout=3000):
                    add_btn.click()
                    print("  ✅ Dataset added")
                else:
                    print("  ⚠️ Could not click Add")
            else:
                print("  ⚠️ Dataset not found in search")
        else:
            print("  ⚠️ Search field not found")
    else:
        print("  ⚠️ Add Data button not found")


def paste_code(page):
    """Paste submission code into notebook"""
    print("📝 Pasting submission code...")
    
    # Read the submission file
    submission_path = Path(__file__).parent.parent / 'hull-tactical-submission.py'
    if not submission_path.exists():
        sys.exit(f"Submission file not found: {submission_path}")
    
    code = submission_path.read_text()
    
    # Find the code editor - Kaggle uses CodeMirror
    editor = page.locator('.CodeMirror, .cm-editor, [data-testid="code-editor"]').first
    if not editor.is_visible(timeout=5000):
        print("  ⚠️ Code editor not found, trying alternative...")
        editor = page.locator('textarea, div[role="textbox"]').first
    
    if editor.is_visible(timeout=3000):
        # Click to focus
        editor.click()
        time.sleep(1)
        
        # Select all and paste
        page.keyboard.press('Control+a')
        time.sleep(0.5)
        
        # Paste the code
        page.keyboard.insert_text(code)
        time.sleep(2)
        print(f"  ✅ Pasted {len(code)} characters")
    else:
        print("  ⚠️ Could not find code editor")


def save_notebook(page):
    """Save the notebook with proper name"""
    print("💾 Saving notebook...")
    
    # Click Save button
    save_btn = page.get_by_text('Save')
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(2)
    
    # Look for title input and set it
    title_input = page.locator('input[placeholder*="title"], input[value="Untitled"]').first
    if title_input.is_visible(timeout=3000):
        title_input.fill(KERNEL_SLUG)
        time.sleep(1)
        print(f"  ✅ Title set to '{KERNEL_SLUG}'")
    
    # Save again with Ctrl+S
    page.keyboard.press('Control+s')
    time.sleep(3)
    print("  ✅ Notebook saved")


def main():
    args = parse_args()
    
    if not args.username or not args.password:
        sys.exit(
            "Please set KAGGLE_USERNAME and KAGGLE_PASSWORD environment variables.\n"
            "Or pass as: --username your@email.com --password yourpass"
        )
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "Playwright not installed.\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
    
    print("=" * 60)
    print("HULL TACTICAL — Create Kernel on Kaggle")
    print("=" * 60)
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()
        
        # Step 1: Login
        login(page, args.username, args.password)
        
        # Step 2: Create notebook
        create_notebook(page)
        
        # Step 3: Add dataset
        add_dataset(page)
        
        # Step 4: Paste code
        paste_code(page)
        
        # Step 5: Save
        save_notebook(page)
        
        print("\n" + "=" * 60)
        print("✅ KERNEL CREATION COMPLETE")
        print("=" * 60)
        print(f"\nNext steps:")
        print(f"  1. Run submit_notebook.py to submit:")
        print(f"     python submit_notebook.py --kernel cwarre33/{KERNEL_SLUG}")
        print(f"         --competition {COMPETITION} --save-session")
        print(f"\n  2. Then submit with --headless for automation")
        
        browser.close()


if __name__ == '__main__':
    main()
