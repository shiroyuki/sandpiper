PY=python3
TEST_FLAGS=-f
PY_TEST=nosetests -x -w .
LXC_TAG_DYNAMODB=sandpiper.test.dynamodb

package:
	$(PY) setup.py sdist

release:
	$(PY) setup.py sdist bdist_wheel upload

# Test all
test: test-inmemory
	@echo "Done"

test-inmemory:
	$(PY_TEST) tests/test_inmemory.py

test-dynamodb:
	$(PY_TEST) tests/test_dynamodb.py

test-dynamodb-docker:
	docker build -q -t $(LXC_TAG_DYNAMODB) lxc/dynamodb > /dev/null && \
		docker run -i -t --rm -v `pwd`:/opt:ro $(LXC_TAG_DYNAMODB)

test-dynamodb-prep-db:
	mkdir -p tmp
	cd tmp && \
		curl --location -O http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz && \
		tar xzf dynamodb_local_latest.tar.gz && \

test-dynamodb-prep-pip:
	pip3 install -q --no-cache-dir --disable-pip-version-check -r requirements.txt

test-dynamodb-docker-prep-db:
	./dynamodb_lxcinner_start > /db/output &

test-dynamodb-docker-runner: test-dynamodb-docker-prep-db test-dynamodb-prep-pip test-dynamodb
	$(PY_TEST) tests/test_dynamodb.py
