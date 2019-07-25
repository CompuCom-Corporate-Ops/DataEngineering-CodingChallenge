CONTAINER_NAME=coding-challenge
TAG_VERSION=latest

build:
	docker build -t $(CONTAINER_NAME):$(TAG_VERSION) .

dev: build
	docker run \
	    -v $(CURDIR)/resources:/coding_challenge/resources                  \
	    -v $(CURDIR)/coding_challenge:/coding_challenge/coding_challenge    \
	    -v $(CURDIR)/tests:/coding_challenge/tests                          \
	    -v $(CURDIR)/requirements.txt:/coding_challenge/requirements.txt    \
	    -v $(CURDIR)/Readme.md:/coding_challenge/Readme.md                  \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                \
	    bash

run: build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    bash

tests: build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    pytest -v

challenge_one: build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    pytest -v tests/test_data_analysis_and_retrieval.py

challenge_two: build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    pytest -v tests/test_application_logic.py

challenge_three: build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    pytest -v tests/test_forecasting.py
