FROM python:3.7

ENV BASE_DIR /coding_challenge
ENV RESOURCE_DIR  $BASE_DIR/resources
ENV CHALLENGE_DIR $BASE_DIR/coding_challenge
ENV TEST_DIR      $BASE_DIR/tests
ENV PYTHONPATH    $BASE_DIR

RUN mkdir -p $BASE_DIR \
             $RESOURCE_DIR \
             $CHALLENGE_DIR \
             $TEST_DIR

COPY resources        $RESOURCE_DIR
COPY requirements.txt $BASE_DIR
COPY Readme.md        $BASE_DIR

RUN  pip install --upgrade -r /coding_challenge/requirements.txt

COPY tests            $TEST_DIR
COPY coding_challenge $CHALLENGE_DIR

WORKDIR $BASE_DIR
