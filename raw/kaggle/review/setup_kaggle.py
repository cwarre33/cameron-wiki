"""
One-time Kaggle setup: upload model dataset + create competition notebook.

Usage:
    KAGGLE_USERNAME=cwarre33 KAGGLE_PASSWORD=yourpassword python setup_kaggle.py

What it does:
    1. Logs in and saves session cookies
    2. Creates private dataset "hull-tactical-model" and uploads hull_dm_model.txt
    3. Creates notebook "hull-tactical-submission" in the competition
    4. Pastes the submission code and links the dataset as input
    5. Saves the notebook (ready to Submit to Competition)
"""

import os, sys, time
from pathlib import Path

MODEL_FILE   = Path(__file__).parent.parent / 'model_files' / 'hull_dm_model.txt'
SUBMISSION   = Path(__file__).parent.parent / 'hull-tactical-submission.py'
SESSION_FILE = Path.home() / '.kaggle' / 'playwright_session.json'
KAGGLE_BASE  = 'https://www.kaggle.com'
USERNAME     = os.environ.get('KAGGLE_USERNAME', 'cwarre33')
PASSWORD     = os.environ.get('KAGGLE_PASSWORD', '')

DATASET_TITLE = 'hull-tactical-model'
KERNEL_TITLE  = 'hull-tactical-submission'
COMPETITION   = 'hull-tactical-market-prediction'


def check_files():
    for f in [MODEL_FILE, SUBMISSION]:
        if not f.exists():
            sys.exit(f"Missing file: {f}")
    print(f"  model:      {MODEL_FILE}  ({MODEL_FILE.stat().st_size:,} bytes)")
    print(f"  submission: {SUBMISSION}")


def login(page):
    print("  Navigating to login...")
    page.goto(f'{KAGGLE_BASE}/account/login', wait_until='networkidle')
    page.get_by_text('Sign in with Email').click()
    page.wait_for_selector('input[name="email"]', timeout=8000)
    page.locator('input[name="email"]').fill(USERNAME)
    page.locator('input[name="password"]').fill(PASSWORD)
    page.get_by_role('button', name='Sign In').last.click()
    page.wait_for_load_state('networkidle', timeout=20000)
    if '/account/login' in page.url:
        page.screenshot(path='/tmp/kaggle_login_fail.png')
        sys.exit("Login failed. Screenshot: /tmp/kaggle_login_fail.png")
    print("  Logged in  ✓")


def is_logged_in(page):
    page.goto(KAGGLE_BASE, wait_until='networkidle')
    return not page.get_by_role('button', name='Sign In').is_visible(timeout=4000)


def save_session(context):
    import json
    cookies = context.cookies()
    SESSION_FILE.parent.mkdir(exist_ok=True)
    SESSION_FILE.write_text(json.dumps(cookies, indent=2))
    print(f"  Session saved → {SESSION_FILE}  ✓")


def load_session(context):
    import json
    if SESSION_FILE.exists():
        context.add_cookies(json.loads(SESSION_FILE.read_text()))
        return True
    return False


# ── Dataset upload ────────────────────────────────────────────────────────────

def create_dataset(page):
    print("\n[2/4] Creating dataset 'hull-tactical-model'...")

    # Check if dataset already exists
    resp = page.goto(f'{KAGGLE_BASE}/{USERNAME}/{DATASET_TITLE}', wait_until='domcontentloaded')
    if resp and resp.status == 200 and 'not found' not in page.title().lower():
        print(f"  Dataset already exists at kaggle.com/{USERNAME}/{DATASET_TITLE}")
        print("  Skipping creation — run 'kaggle datasets version' to update.")
        return

    page.goto(f'{KAGGLE_BASE}/datasets/new', wait_until='networkidle')
    time.sleep(2)

    # Upload file via file input
    file_input = page.locator('input[type="file"]')
    if not file_input.is_visible(timeout=5000):
        # Some layouts hide the input — look for the drop zone and make input visible
        page.evaluate("document.querySelectorAll('input[type=file]').forEach(el => el.style.display='block')")
    file_input.set_input_files(str(MODEL_FILE))
    print(f"  Uploading {MODEL_FILE.name}...")
    time.sleep(3)  # wait for upload progress

    # Set dataset title
    title_input = page.locator('input[placeholder*="title"], input[name="title"], input[id*="title"]').first
    if title_input.is_visible(timeout=5000):
        title_input.triple_click()
        title_input.fill(DATASET_TITLE)

    # Set to private
    private_option = page.get_by_role('radio', name='Private').or_(
        page.locator('label:has-text("Private") input[type="radio"]')
    )
    if private_option.is_visible(timeout=3000):
        private_option.first.click()

    # Accept license if shown
    license_accept = page.locator('button:has-text("I Understand"), button:has-text("Accept")')
    if license_accept.is_visible(timeout=2000):
        license_accept.click()

    # Click Create
    create_btn = page.get_by_role('button', name='Create').or_(
        page.locator('button:has-text("Create Dataset")')
    )
    create_btn.first.click()
    page.wait_for_load_state('networkidle', timeout=30000)
    time.sleep(2)

    if USERNAME in page.url and DATASET_TITLE in page.url:
        print(f"  Dataset created: {page.url}  ✓")
    else:
        page.screenshot(path='/tmp/kaggle_dataset_fail.png')
        print(f"  Unexpected URL after create: {page.url}")
        print(f"  Screenshot: /tmp/kaggle_dataset_fail.png")
        print("  Check manually, then re-run or continue to step 3.")


# ── Notebook creation ─────────────────────────────────────────────────────────

def create_notebook(page):
    print(f"\n[3/4] Creating notebook '{KERNEL_TITLE}'...")

    # Check if notebook already exists
    resp = page.goto(f'{KAGGLE_BASE}/code/{USERNAME}/{KERNEL_TITLE}', wait_until='domcontentloaded')
    if resp and resp.status == 200 and 'not found' not in page.title().lower():
        print(f"  Notebook already exists at kaggle.com/code/{USERNAME}/{KERNEL_TITLE}")
        print("  Opening editor to verify/update code...")
        edit_btn = page.locator('button:has-text("Edit"), a:has-text("Edit")')
        if edit_btn.is_visible(timeout=5000):
            edit_btn.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
        return patch_notebook(page)

    # Start new notebook from competition page
    page.goto(f'{KAGGLE_BASE}/competitions/{COMPETITION}/code', wait_until='networkidle')
    time.sleep(2)

    new_nb_btn = page.get_by_role('button', name='New Notebook').or_(
        page.locator('a:has-text("New Notebook"), button:has-text("New Notebook")')
    )
    if not new_nb_btn.is_visible(timeout=8000):
        page.screenshot(path='/tmp/kaggle_newnotebook.png')
        print("  'New Notebook' button not found. Screenshot: /tmp/kaggle_newnotebook.png")
        print("  Navigate manually: competition → Code tab → New Notebook")
        return

    new_nb_btn.first.click()
    page.wait_for_load_state('networkidle', timeout=20000)
    time.sleep(4)
    print("  Editor opened  ✓")
    patch_notebook(page)


def patch_notebook(page):
    print("[3b/4] Pasting submission code...")
    code = SUBMISSION.read_text()

    # The Kaggle editor is CodeMirror — click into it, select all, replace
    editor = page.locator('.CodeMirror, [class*="editor"], .cm-content').first
    if not editor.is_visible(timeout=8000):
        page.screenshot(path='/tmp/kaggle_editor.png')
        print("  Editor not found. Screenshot: /tmp/kaggle_editor.png")
        print("  Paste manually from: raw/kaggle/hull-tactical-submission.py")
        return

    editor.click()
    time.sleep(0.5)
    # Select all and replace
    page.keyboard.press('Meta+A' if sys.platform == 'darwin' else 'Control+A')
    time.sleep(0.3)
    page.keyboard.type(code, delay=0)  # delay=0 = fast paste
    time.sleep(2)
    print("  Code pasted  ✓")

    add_dataset(page)
    save_notebook(page)


def add_dataset(page):
    print("[3c/4] Adding dataset as input...")
    # Look for "Add data" or the data panel
    add_data_btn = page.locator(
        'button:has-text("Add Data"), button:has-text("+ Add Data"), '
        '[aria-label*="Add data"], button:has-text("Data")'
    ).first
    if not add_data_btn.is_visible(timeout=5000):
        print("  'Add Data' button not found — add dataset manually:")
        print(f"    Search for: {USERNAME}/{DATASET_TITLE}")
        return

    add_data_btn.click()
    time.sleep(2)

    # Search for our dataset
    search = page.locator('input[placeholder*="Search"], input[type="search"]').first
    if search.is_visible(timeout=5000):
        search.fill(f'{USERNAME}/{DATASET_TITLE}')
        time.sleep(1.5)

    # Click the dataset result
    result = page.locator(f'text={DATASET_TITLE}').first
    if result.is_visible(timeout=5000):
        result.click()
        time.sleep(1)
        add_btn = page.get_by_role('button', name='Add').or_(
            page.locator('button:has-text("Add to Notebook")')
        )
        if add_btn.is_visible(timeout=3000):
            add_btn.first.click()
            time.sleep(1)
            print(f"  Dataset '{DATASET_TITLE}' added  ✓")
    else:
        print(f"  Dataset result not found. Add manually: {USERNAME}/{DATASET_TITLE}")


def save_notebook(page):
    print("[3d/4] Saving notebook...")
    # Cmd/Ctrl+S to save
    page.keyboard.press('Meta+S' if sys.platform == 'darwin' else 'Control+S')
    time.sleep(3)

    # Also look for explicit Save button
    save_btn = page.locator('button:has-text("Save Version"), button:has-text("Save")').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(2)
        # Confirm quick save if dialog appears
        quick_save = page.locator('button:has-text("Save"), label:has-text("Save & Run All")').first
        if quick_save.is_visible(timeout=3000):
            quick_save.click()
            time.sleep(2)

    print(f"  Notebook saved: {page.url}  ✓")
    print(f"\n  Next: run submit_notebook.py to submit to competition")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not PASSWORD:
        sys.exit(
            "KAGGLE_PASSWORD not set.\n"
            "  KAGGLE_USERNAME=cwarre33 KAGGLE_PASSWORD=yourpassword python setup_kaggle.py"
        )

    print("=== Hull Tactical — one-time Kaggle setup ===\n")
    print("[0/4] Checking files...")
    check_files()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("pip install playwright && playwright install chromium")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)  # visible so you can intervene if needed
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        print("\n[1/4] Authenticating...")
        load_session(context)
        if not is_logged_in(page):
            login(page)
        save_session(context)

        create_dataset(page)
        create_notebook(page)

        print("\n[4/4] Done. Review the browser, then close it.")
        print("  If anything looks wrong, fix it manually before submitting.")
        input("  Press Enter to close the browser...")
        browser.close()


if __name__ == '__main__':
    main()
