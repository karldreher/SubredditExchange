TAG=${WHOAMI}-subreddit-exchange
WHOAMI := $(shell who | awk '{print $$1}')

docker_build:
	docker build -t $(TAG) .

docker_run: docker_build
	docker run --rm -it -p 80 $(TAG)

docker_run_sh: docker_build
	docker run --rm -it -p 80 --entrypoint sh $(TAG)
