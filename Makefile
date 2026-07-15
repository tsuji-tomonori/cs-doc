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
	@pages=$$(pdfinfo $(PUBLIC_PDF) | awk '/^Pages:/ {print $$2}'); test "$$pages" -ge 170
	@urls=$$(pdfinfo -url $(PUBLIC_PDF) | awk 'NR > 1 {print $$3}' | sort -u | wc -l); test "$$urls" -ge 35
	@printf '検証完了: %sページ、外部リンク%s件\n' "$$(pdfinfo $(PUBLIC_PDF) | awk '/^Pages:/ {print $$2}')" "$$(pdfinfo -url $(PUBLIC_PDF) | awk 'NR > 1 {print $$3}' | sort -u | wc -l)"

site: pdf
	mkdir -p $(SITE_DIR)
	cp $(PUBLIC_PDF) $(SITE_DIR)/information-engineering-basics.pdf

clean:
	TEXMFVAR=$(TEXMFVAR) TEXMFCACHE=$(TEXMFCACHE) $(LATEXMK) -C -outdir=$(BUILD_DIR) $(MAIN)
	rm -f $(PUBLIC_PDF) $(SITE_DIR)/information-engineering-basics.pdf
