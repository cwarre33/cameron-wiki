"""
Kaggle notebook competition submitter — reusable across competitions.

Automates: login → open kernel editor → click "Submit to Competition".
Works for any competition that uses the notebook/interactive-API submission model.

Usage:
    # First run (saves session cookies so you don't re-login each week):
    python submit_notebook.py \\
        --kernel cwarre33/hull-tactical-submission \\
        --competition hull-tactical-market-prediction \\
        --save-session

    # Subsequent runs (reuses saved session):
    python submit_notebook.py \\
        --kernel cwarre33/hull-tactical-submission \\
        --competition hull-tactical-market-prediction

    # Headless (for cron):
    python submit_notebook.py --kernel ... --competition ... --headless

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

SESSION_FILE = Path.home() / '.kaggle' / 'playwright_session.json'
KAGGLE_BASE = 'https://www.kaggle.com'


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--kernel', required=True, help='username/kernel-slug')
    p.add_argument('--competition', required=True, help='competition slug')
    p.add_argument('--headless', action='store_true', help='run without browser window')
    p.add_argument('--save-session', action='store_true', help='save cookies after login')
    p.add_argument('--username', default=os.getenv('KAGGLE_USERNAME'))
    p.add_argument('--password', default=os.getenv('KAGGLE_PASSWORD'))
    return p.parse_args()


def login(page, username: str, password: str):
    print("  Logging in...")
    page.goto(f'{KAGGLE_BASE}/account/login')
    page.wait_for_load_state('networkidle')

    # Handle Google login prompt if present — use email/password instead
    email_field = page.locator('input[name="email"]')
    if email_field.is_visible(timeout=3000):
        email_field.fill(username)
        page.locator('input[name="password"]').fill(password)
        page.locator('button[type="submit"]').click()
    else:
        # Sign in with email link
        page.locator('text=Sign in with Email').click()
        page.locator('input[name="email"]').fill(username)
        page.locator('input[name="password"]').fill(password)
        page.locator('button[type="submit"]').click()

    page.wait_for_load_state('networkidle', timeout=15000)
    if 'login' in page.url:
        sys.exit("Login failed — check KAGGLE_USERNAME / KAGGLE_PASSWORD env vars.")
    print("  Logged in.")


def load_session(context):
    if SESSION_FILE.exists():
        cookies = json.loads(SESSION_FILE.read_text())
        context.add_cookies(cookies)
        print(f"  Loaded session from {SESSION_FILE}")
        return True
    return False


def save_session(context):
    cookies = context.cookies()
    SESSION_FILE.parent.mkdir(exist_ok=True)
    SESSION_FILE.write_text(json.dumps(cookies, indent=2))
    print(f"  Session saved to {SESSION_FILE}")


def is_logged_in(page) -> bool:
    page.goto(KAGGLE_BASE, wait_until='networkidle')
    return page.locator('[data-testid="user-avatar"]').is_visible(timeout=4000)


def open_kernel_and_submit(page, kernel_slug: str, competition_slug: str):
    kernel_url = f'{KAGGLE_BASE}/code/{kernel_slug}'
    print(f"  Opening kernel: {kernel_url}")
    page.goto(kernel_url, wait_until='networkidle')
    time.sleep(2)

    # Click Edit to open the kernel editor
    edit_btn = page.locator('button:has-text("Edit"), a:has-text("Edit")')
    if edit_btn.is_visible(timeout=5000):
        edit_btn.first.click()
        page.wait_for_load_state('networkidle', timeout=20000)
        time.sleep(3)
        print("  Opened editor.")
    else:
        print("  Already in editor or Edit button not found — continuing.")

    # Look for "Submit to Competition" button (Kaggle's notebook editor)
    submit_btn = page.locator(
        'button:has-text("Submit to Competition"), '
        '[data-testid="submit-to-competition-button"]'
    )

    if not submit_btn.is_visible(timeout=10000):
        # Try the "..." menu / Run dropdown
        run_menu = page.locator('button[aria-label="Run"], button:has-text("Run")')
        if run_menu.is_visible(timeout=3000):
            run_menu.first.click()
            time.sleep(1)
            submit_btn = page.locator('text=Submit to Competition')

    if not submit_btn.is_visible(timeout=5000):
        page.screenshot(path='/tmp/kaggle_submit_debug.png')
        sys.exit(
            "Could not find 'Submit to Competition' button. "
            "Screenshot saved to /tmp/kaggle_submit_debug.png — check manually."
        )

    print("  Clicking 'Submit to Competition'...")
    submit_btn.first.click()
    time.sleep(2)

    # Confirm dialog if present
    confirm = page.locator('button:has-text("Submit"), button:has-text("Confirm")')
    if confirm.is_visible(timeout=4000):
        confirm.first.click()
        print("  Confirmed submission.")

    # Wait for submission to register
    page.wait_for_load_state('networkidle', timeout=30000)
    time.sleep(3)

    # Check for success indicator
    success = page.locator('text=Submission complete, text=submitted, text=Queued')
    if success.is_visible(timeout=10000):
        print(f"  Submission successful for competition: {competition_slug}")
    else:
        page.screenshot(path='/tmp/kaggle_submit_result.png')
        print(
            "  Could not confirm success — check /tmp/kaggle_submit_result.png. "
            "Submission may still have gone through."
        )


def main():
    args = parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "Playwright not installed.\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        session_loaded = load_session(context)

        if session_loaded and is_logged_in(page):
            print("  Session valid — skipping login.")
        else:
            if not args.username or not args.password:
                sys.exit(
                    "No valid session and no credentials provided.\n"
                    "Set KAGGLE_USERNAME and KAGGLE_PASSWORD env vars, or run with --save-session once."
                )
            login(page, args.username, args.password)
            if args.save_session:
                save_session(context)

        open_kernel_and_submit(page, args.kernel, args.competition)
        browser.close()


if __name__ == '__main__':
    main()
