PY=python3
TEST_FLAGS=-f
PY_TEST=nosetests -x -w .
LXC_TAG_DYNAMODB=sandpiper.test.dynamodb

LXC_TAG_MEMCACHED=memcached:latest
LXC_NAME_MEMCACHED=sandpiper.memcached

LXC_TAG_REDIS_V2=redis:2
LXC_NAME_REDIS_V2=sandpiper.redis.v2

LXC_TAG_REDIS_LATEST=redis:latest
LXC_NAME_REDIS_LATEST=sandpiper.redis.latest

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

test-memcached:
	$(PY_TEST) tests/test_memcached.py

test-xredis:
	$(PY_TEST) tests/test_xredis.py

test-dynamodb-docker:
	docker build -t $(LXC_TAG_DYNAMODB) lxc/dynamodb && \
		docker run -i -t --rm --privileged -v `pwd`:/opt:ro $(LXC_TAG_DYNAMODB)

test-dynamodb-prep-db:
	mkdir -p tmp
	cd tmp && \
		curl --location -O http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz && \
		tar xzf dynamodb_local_latest.tar.gz && \

test-dynamodb-prep-pip:
	pip3 install -q --no-cache-dir --disable-pip-version-check -r requirements-test.txt

test-dynamodb-docker-prep-db:
	./dynamodb_lxcinner_start > /db/output &

test-dynamodb-docker-runner: test-dynamodb-docker-prep-db test-dynamodb-prep-pip test-dynamodb
	@echo "Done"

test-memcached-docker:
	@docker rm -f $(LXC_NAME_MEMCACHED); \
		docker run -d --name $(LXC_NAME_MEMCACHED) -p 11211:11211 $(LXC_TAG_MEMCACHED)
	make test-memcached
	@docker rm -f $(LXC_NAME_MEMCACHED)

test-xredis-v2-docker:
	@docker rm -f $(LXC_NAME_REDIS_V2); \
		docker run -d --name $(LXC_NAME_REDIS_V2) -p 6379:6379 $(LXC_TAG_REDIS_V2)
	make test-xredis
	@docker rm -f $(LXC_NAME_REDIS_V2)

test-xredis-latest-docker:
	@docker rm -f $(LXC_NAME_REDIS_LATEST); \
		docker run -d --name $(LXC_NAME_REDIS_LATEST) -p 6379:6379 $(LXC_TAG_REDIS_LATEST)
	make test-xredis
	@docker rm -f $(LXC_NAME_REDIS_LATEST)
