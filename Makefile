LATEXMK ?= latexmk
MAIN := main.tex
BUILD_DIR := build
PDF := $(BUILD_DIR)/main.pdf
PUBLIC_PDF := $(BUILD_DIR)/information-engineering-basics.pdf
LOG := $(BUILD_DIR)/main.log
SITE_DIR := site
TEXMFVAR := $(CURDIR)/$(BUILD_DIR)/texmf-var
TEXMFCACHE := $(CURDIR)/$(BUILD_DIR)/texmf-cache

.PHONY: all pdf verify site clean

all: pdf

pdf:
	mkdir -p $(BUILD_DIR)
	TEXMFVAR=$(TEXMFVAR) TEXMFCACHE=$(TEXMFCACHE) $(LATEXMK) -lualatex -interaction=nonstopmode -halt-on-error -outdir=$(BUILD_DIR) $(MAIN)
	cp $(PDF) $(PUBLIC_PDF)

verify: pdf
	@if grep -En 'Overfull|Underfull|LaTeX (Font )?Warning|Package .* Warning|Undefined control sequence|Missing character' $(LOG); then exit 1; fi
	@pages=$$(pdfinfo $(PUBLIC_PDF) | awk '/^Pages:/ {print $$2}'); test "$$pages" -ge 90
	@pdfinfo $(PUBLIC_PDF) | grep -q 'Page size:.*A4'
	@urls=$$(pdfinfo -url $(PUBLIC_PDF) | awk 'NR > 1 {print $$3}' | sort -u | wc -l); test "$$urls" -ge 35
	@if grep -ERn '\\begin\{frame\}|\\begin\{columns\}|\\chapterframe' main.tex chapters tex; then exit 1; fi
	@if grep -En '^\\(chapter|section)\{.*(です|ます|ません)\}' chapters/*.tex; then exit 1; fi
	@itemize=$$(grep -h '^[[:space:]]*\\begin{itemize}' chapters/0[1-7]-*.tex | wc -l); test "$$itemize" -le 1
	@sections=$$(grep -h '^\\section{' chapters/*.tex | wc -l); test "$$sections" -ge 160
	@chars=$$(pdftotext $(PUBLIC_PDF) - | wc -m); test "$$chars" -ge 60000
	@pdffonts $(PUBLIC_PDF) | awk 'NR > 2 && $$(NF-4) != "yes" {exit 1}'
	@printf '読み物版検証完了: %sページ、本文%s文字、外部リンク%s件\n' \
	  "$$(pdfinfo $(PUBLIC_PDF) | awk '/^Pages:/ {print $$2}')" \
	  "$$(pdftotext $(PUBLIC_PDF) - | wc -m)" \
	  "$$(pdfinfo -url $(PUBLIC_PDF) | awk 'NR > 1 {print $$3}' | sort -u | wc -l)"

site: pdf
	mkdir -p $(SITE_DIR)
	cp $(PUBLIC_PDF) $(SITE_DIR)/information-engineering-basics.pdf

clean:
	TEXMFVAR=$(TEXMFVAR) TEXMFCACHE=$(TEXMFCACHE) $(LATEXMK) -C -outdir=$(BUILD_DIR) $(MAIN)
	rm -f $(PUBLIC_PDF) $(SITE_DIR)/information-engineering-basics.pdf
