.PHONY: run stat report clean
OBJ = lab1.py

run: ${OBJ}
	python ${OBJ}

stat: ${OBJ}
	pycodestyle -v ${OBJ} > pep8 || \
	coverage run ${OBJ}
	coverage report -m > coverage

report: stat
	cat pep8 coverage

clean:
	rm pep8 coverage .coverage