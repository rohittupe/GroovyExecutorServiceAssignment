.PHONY : environment test clean

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
JAR_NAME = product-qa-groovy
JAR_VERSION = 1.0.1
JAR_FILE = $(JAR_NAME)-$(JAR_VERSION)

environment: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

start-server:
	java -jar $(JAR_FILE).jar

test:
	$(PYTHON) -m pytest --html=./reports/report.html -capture=tee-sys  --self-contained-html -vv -n 2 --environment=local .


clean:
	rm -rf __pycache__
	rm -rf $(VENV)

stop-server:
	sh stop-server.sh

