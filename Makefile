.PHONY: all release clean docs babel-all babel-new

all: clean

release:
	python setup.py release sdist upload

clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.swp' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info

docs:
	$(MAKE) -C docs html

babel-all:
	@python setup.py extract_messages
	@python setup.py update_catalog
	@python setup.py compile_catalog

babel-new:
	@python setup.py init_catalog -l $(LANG)
