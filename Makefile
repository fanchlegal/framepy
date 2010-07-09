.PHONY: all release clean docs

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

