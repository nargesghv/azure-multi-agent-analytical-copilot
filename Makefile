install:
	pip install -r requirements.txt

run:
	uvicorn app.api.main:app --reload

test:
	pytest

docker-build:
	docker build -t analytical-copilot .