REQUIREMENTS_FILE := 'requirements.txt'
TEST_REQUIREMENTS_FILE := 'test-requirements.txt'

.PHONY: init freeze dev start

init:
	pip install -r $(REQUIREMENTS_FILE)


freeze:
	pip freeze > $(REQUIREMENTS_FILE)


test-init:
	pip install -r $(TEST_REQUIREMENTS_FILE)


freeze-test:
	pip freeze > $(TEST_REQUIREMENTS_FILE)


dev:
	uvicorn app.main:app --reload --port 3030


start:
	python3 -m app.main
