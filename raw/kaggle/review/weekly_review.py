#!/usr/bin/env python3
"""
Hull Tactical — Weekly Review Pipeline

Checks:
1. Leaderboard (top 10)
2. Your submissions
3. Prompts for retrain/submit cycle

Usage:
    python weekly_review.py
    
Env:
    KAGGLE_TOKEN (Bearer token KGAT_...)
"""
import json
import os
import urllib.request

# === Config ===
COMPETITION = "hull-tactical-market-prediction"
KERNEL_USER = "cwarre33"
KERNEL_SLUG = "hull-tactical-submission"
KAGGLE_TOKEN = os.getenv("KAGGLE_TOKEN", "KGAT_4b641e87a3d05d023dc387fc63758ee0")
AUTH_HEADER = f"Bearer {KAGGLE_TOKEN}"


def api_call(url: str) -> dict:
    """Make API request with proper auth"""
    req = urllib.request.Request(url, headers={'Authorization': AUTH_HEADER})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def check_leaderboard():
    """Print top 10 leaderboard"""
    print("\n📊 LEADERBOARD (Top 10):")
    print("-" * 50)
    try:
        data = api_call(f"https://www.kaggle.com/api/v1/competitions/{COMPETITION}/leaderboard/view")
        teams = data.get('submissions', [])[:10]
        for i, t in enumerate(teams, 1):
            score = str(t.get('score', '?'))[:10] if t.get('score') else '    ?'
            name = t.get('teamName', '?')[:25]
            you = " ← YOU" if t.get('teamName', '').lower().replace(' ', '') == KERNEL_USER.lower() else ""
            print(f"  {i:2d}. {name:<25} {score}{you}")
        if teams:
            print(f"\n  Target to beat: Sharpe = {teams[0].get('score', '?')}")
    except Exception as e:
        print(f"  Error: {e}")


def check_submissions():
    """Print your submissions"""
    print("\n🎯 YOUR SUBMISSIONS:")
    print("-" * 50)
    try:
        data = api_call(f"https://www.kaggle.com/api/v1/competitions/{COMPETITION}/submissions/list")
        if isinstance(data, list) and len(data) > 0:
            for s in data[:10]:
                date = s.get('date', '?')[:10]
                score = s.get('publicScore', '?')
                status = s.get('status', '?')
                print(f"  {date}  Sharpe={score}  [{status}]")
        else:
            print("  ❌ No submissions found")
    except Exception as e:
        print(f"  ❌ No submissions yet")
        print(f"\n  Error: {e}")


def check_kernel():
    """Check kernel status"""
    print("\n🔧 KERNEL STATUS:")
    print("-" * 50)
    try:
        data = api_call(f"https://www.kaggle.com/api/v1/kernels/pull")
        print(f"  Kernel exists: {data.get('title', '?')}")
        print(f"  Version: {data.get('currentVersionNumber', '?')}")
        print(f"  Status: {data.get('status', '?')}")
    except Exception as e:
        print(f"  ⚠️ Kernel not found (need to create first)")


def print_actions():
    """Show next actions"""
    print("\n⚡ NEXT ACTIONS:")
    print("-" * 50)
    print("""
  To make your first submission:
  
  1. MANUAL SETUP (one-time on Kaggle):
     - Create notebook at kaggle.com/competitions/hull-tactical-market-prediction
     - Add dataset cwarre33/hull-tactical-model as input
     - Paste content from hull-tactical-submission.py
     - Save as 'hull-tactical-submission'
  
  2. SETUP AUTH:
     export KAGGLE_USERNAME=YOUR_EMAIL
     export KAGGLE_PASSWORD=YOUR_PASSWORD
     python submit_notebook.py --kernel cwarre33/hull-tactical-submission \\
         --competition hull-tactical-market-prediction --save-session
  
  3. SUBMIT (after session saved):
     python submit_notebook.py --kernel cwarre33/hull-tactical-submission \\
         --competition hull-tactical-market-prediction --headless
  
  Weekly review this script: ./weekly_review.py
""")


def main():
    print("=" * 60)
    print("HULL TACTICAL WEEKLY REVIEW")
    print("=" * 60)
    
    check_leaderboard()
    check_submissions()
    print_actions()
    
    print("=" * 60)


if __name__ == '__main__':
    main()
