PACKAGE := pytablereader
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	python setup.py check
	codespell $(PACKAGE) docs examples test -q 2 --check-filenames --ignore-words-list te --exclude-file "test/data/python - Wiktionary.html"
	travis lint
	pylama

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@tox -e docs

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && tox -e readme

.PHONY: release
release:
	@tox -e release
	@make clean
