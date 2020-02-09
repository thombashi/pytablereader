PACKAGE := pytablereader
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


.PHONY: build
build:
	@make clean
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@python setup.py clean --all
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
	@python setup.py build_sphinx --source-dir=$(DOCS_DIR)/ --build-dir=$(DOCS_BUILD_DIR) --all-files

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && tox -e readme

.PHONY: release
release:
	@python setup.py release --sign
	@make clean
