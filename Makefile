LATEXMK ?= latexmk
MAIN := main.tex
BUILD_DIR := build
PDF := $(BUILD_DIR)/main.pdf
PUBLIC_PDF := $(BUILD_DIR)/information-engineering-basics.pdf
TEXMFVAR := $(CURDIR)/$(BUILD_DIR)/texmf-var
TEXMFCACHE := $(CURDIR)/$(BUILD_DIR)/texmf-cache

.PHONY: all pdf clean site

all: pdf

pdf:
	mkdir -p $(BUILD_DIR)
	TEXMFVAR=$(TEXMFVAR) TEXMFCACHE=$(TEXMFCACHE) $(LATEXMK) -lualatex -interaction=nonstopmode -halt-on-error -outdir=$(BUILD_DIR) $(MAIN)
	cp $(PDF) $(PUBLIC_PDF)

site: pdf
	mkdir -p site
	cp $(PUBLIC_PDF) site/information-engineering-basics.pdf

clean:
	TEXMFVAR=$(TEXMFVAR) TEXMFCACHE=$(TEXMFCACHE) $(LATEXMK) -C -outdir=$(BUILD_DIR) $(MAIN)
	rm -f $(PUBLIC_PDF) site/information-engineering-basics.pdf
