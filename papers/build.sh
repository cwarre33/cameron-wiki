#!/bin/bash
# Build script for arXiv-compatible papers
# Usage: ./papers/build.sh paper-name
# Run from repo root

set -e

PAPER_NAME="${1:-main}"

# Get paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR"
BUILD_DIR="$SCRIPT_DIR/builds"

echo "=== Building: $PAPER_NAME ==="
echo "Source dir: $SOURCE_DIR"
mkdir -p "$BUILD_DIR"

# Find source file
if [ -f "$SOURCE_DIR/$PAPER_NAME.tex" ]; then
  SRC="$SOURCE_DIR/$PAPER_NAME.tex"
elif [ -f "$SOURCE_DIR/$PAPER_NAME/$PAPER_NAME.tex" ]; then
  SRC="$SOURCE_DIR/$PAPER_NAME/$PAPER_NAME.tex"
else
  echo "Error: Cannot find $PAPER_NAME.tex in $SOURCE_DIR"
  ls -la "$SOURCE_DIR/"
  exit 1
fi

echo "Source: $SRC"

# Determine engine
if grep -q "fontspec" "$SRC" 2>/dev/null || \
   grep -q "unicode-math" "$SRC" 2>/dev/null; then
  ENGINE="xelatex"
  echo "Engine: XeLaTeX"
else
  ENGINE="pdflatex"
  echo "Engine: pdfLaTeX"
fi

# Build in source dir for relative paths to work
cd "$SOURCE_DIR"
echo "Working in: $(pwd)"

# Clean old build files
rm -f "$BUILD_DIR/$PAPER_NAME".{pdf,aux,log,bbl,blg}

# First pass
echo "=== Pass 1/3 ==="
$ENGINE -interaction=nonstopmode -halt-on-error \
  -output-directory="$BUILD_DIR" \
  "$(basename "$SRC")" 2>&1 | tee "$BUILD_DIR/build.log" | grep -E "^(LaTeX Warning|Output|!)" || true

# Bibliography
if [ -f "$BUILD_DIR/$PAPER_NAME.aux" ]; then
  if grep -q "bibdata" "$BUILD_DIR/$PAPER_NAME.aux" 2>/dev/null; then
    echo "=== BibTeX ==="
    cd "$BUILD_DIR"
    bibtex "$PAPER_NAME" 2>&1 | tail -5 || true
    cd "$SOURCE_DIR"
  fi
fi

# Second pass
echo "=== Pass 2/3 ==="
$ENGINE -interaction=nonstopmode -halt-on-error \
  -output-directory="$BUILD_DIR" \
  "$(basename "$SRC")" 2>&1 | tail -3

# Final pass
echo "=== Pass 3/3 ==="
$ENGINE -interaction=nonstopmode -halt-on-error \
  -output-directory="$BUILD_DIR" \
  "$(basename "$SRC")" 2>&1 | tail -3

# Results
if [ -f "$BUILD_DIR/$PAPER_NAME.pdf" ]; then
  PAGES=$(pdfinfo "$BUILD_DIR/$PAPER_NAME.pdf" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
  SIZE=$(du -h "$BUILD_DIR/$PAPER_NAME.pdf" | cut -f1)
  echo ""
  echo "✓ Build successful"
  echo "PDF: $BUILD_DIR/$PAPER_NAME.pdf"
  echo "Pages: $PAGES"
  echo "Size: $SIZE"
  
  # Copy to papers/ root
  cp "$BUILD_DIR/$PAPER_NAME.pdf" "$SOURCE_DIR/"
  echo "Also: $SOURCE_DIR/$PAPER_NAME.pdf"
else
  echo "✗ Build FAILED"
  tail -50 "$BUILD_DIR/build.log"
  exit 1
fi
