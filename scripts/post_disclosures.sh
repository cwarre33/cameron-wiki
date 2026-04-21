#!/bin/bash
# One-click disclosure poster helper
# Usage: ./post_disclosures.sh

echo "🚀 GitHub Security Disclosure Quick Poster"
echo "=========================================="
echo ""
echo "Make sure you're logged into GitHub in your browser"
echo ""

POSTS=(
  "1|codename-co/devs|CRITICAL|🚨 CRITICAL: GitHub Token + Database Credentials Exposed"
  "2|ayoubagrebi062-hue/olympus-2.0|HIGH|CRITICAL: Multiple Exposed Secrets in Repository"
  "3|openworkflowdev/openworkflow|HIGH|Security Alert: PostgreSQL Credentials Exposed"
  "4|pplcallmesatz/svgtofont|HIGH|Security Disclosure: Database Credentials Exposed"
  "5|atuinsh/atuin|MEDIUM|Security Disclosure: Exposed Token Pattern in secrets.rs"
)

for post in "${POSTS[@]}"; do
  IFS='|' read -r num repo severity title <<< "$post"
  echo "[$num] $repo ($severity)"
  echo "    URL: https://github.com/$repo/issues/new"
  echo "    Title: $title"
  echo ""
done

echo "=========================================="
echo "Copy-paste templates are in:"
echo "  docs/READY_TO_POST_DISCLOSURES.md"
echo ""
echo "Recommended order: 1 → 2 → 3 → 4 → 5"
echo ""

# Open browser URLs
read -p "Open all 5 issue pages in browser? (y/n): " answer
if [[ $answer == "y" ]]; then
  for post in "${POSTS[@]}"; do
    IFS='|' read -r num repo severity title <<< "$post"
    open "https://github.com/$repo/issues/new" 2>/dev/null || xdg-open "https://github.com/$repo/issues/new" 2>/dev/null || echo "Open: https://github.com/$repo/issues/new"
    sleep 0.5
  done
fi
