all: build

clean:
	rm -rf build
	rm -rf dist

build: clean
	python3 -m build -w

uninstall: 
	pip uninstall -y gh-hosts

install: build uninstall
	pip install dist/*.whl

upload: build
	twine upload -r local ./dist/*.whl