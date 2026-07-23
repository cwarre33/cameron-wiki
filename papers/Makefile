# Makefile for arXiv papers
# Usage: make PAPER=sample-osint-paper

PAPER = sample-osint-paper
BUILD_DIR = ./builds

.PHONY: all clean

all: $(BUILD_DIR)/$(PAPER).pdf

$(BUILD_DIR)/%.pdf: %.tex
	@mkdir -p $(BUILD_DIR)
	pdflatex -interaction=nonstopmode -output-directory=$(BUILD_DIR) $<
	cp $(BUILD_DIR)/$*.pdf ./$*.pdf
	@echo "Built: $*.pdf"

clean:
	rm -rf $(BUILD_DIR)/*
	rm -f *.pdf
