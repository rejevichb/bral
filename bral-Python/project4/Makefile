# Makefile
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv --python /usr/bin/python3  venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
	source venv/bin/activate