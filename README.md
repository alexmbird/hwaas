Hello World as a Service
========================

Toy hello-world printing service using the Python-Requests framework.



## General Information

|          |  |
|---------------|------|
| __Service name__  | `hw-worker` &amp; `hw-client` |
| __Default ports__ | None; communicates via Redis |
| __Config files__  | None; uses env vars with sensible defaults |



## Configuration Options

### For hw-worker

| Type | Key | Default value | Notes |
|------|-----|---------------|-------|
| env | `REDIS_URL`  | `redis://localhost:6379/1` | |

### For hw-client

| Type | Key | Default value | Notes |
|------|-----|---------------|-------|
| env | `REDIS_URL`  | `redis://localhost:6379/1` | |

### For Redis

...anything the Docker [redis](https://hub.docker.com/_/redis/) library image accepts.


## Rationale

We want to make Hello World as a Service (HWaaS.) For some stupid reason, clients are actually paying us to print "hello, world!" repeatedly in the terminal. Because we want to be webscale, we'll use rq, which will allow us to have multiple servers printing hello world, and multiple clients submitting requests to print hello world.

Please write the following:

* A function that simply prints the only argument given to it
* A client that, once a second, calls this function via rq to print "hello, world!"
* A script for starting HWaaS, including the rq worker and the client.
    * On dev machines, we'll execute it like so: `./hwaas 1 1`, which will start 1 rq worker, and 1 client. This will print hello world once a second, allowing the devs to easily debug and improve the application.
    * On prod, we'll execute it like so: `./hwaas 10 1000`, which will start 10 servers, and 1000 clients. This will print hello world a thousand times a second, which will make the clients pay us a lot of money.

Feel free to use your choice of containerization of other technologies for the script. However it's important that

* This script is trivially runnable on mac, i.e. the user should not need to install redis, rq, etc. to get up and running. They should be able to just run `hwaas`.
* There's minimal risk of dropped hello worlds if a lot of rq workers / clients are running.



## Running

### Under docker-compose

This is the recommended method for development.

Requirements:

*   Docker.  Docker-for-mac is [here](https://docs.docker.com/docker-for-mac/).

A single worker/client pair:

```bash
$ docker-compose build   # pick up any changes to the codebase
$ docker-compose up
     ...runs until Ctrl+C
$ docker-compose down
```

To get more instances of running services (in another terminal):

```bash
$ docker-compose scale hw-client=4
```



### Staging/Production

The recommended method for any time you need it on a server.

TBD: k8s or Amazon ECS tooling.


### Hacking

To run the codebases locally (i.e. outside of Docker)...

Setting up:

```bash
$ pyvenv _venv
$ . _venv/bin/activate
$ pip install -r src/requirements.txt
```

Running the worker:

```bash
$ _venv/bin/activate
$ python3 src/hwserver.py
```

Running the client:

```bash
$ _venv/bin/activate
$ cd src
$ rq worker --quiet -c worker_settings
```


## Implementation Notes

*  Why Alpine rather than Ubuntu for the Docker container?  Because it's a cut-down Linux designed to have a small footprint, which is ideal for keeping deployable container size down.
*  For each container:
    * The target process runs as a non-root user, specified with the Dockerfile's `USER` statement.  This greatly improves security by restricting the access it has to the kernel's syscall interfaces.
    * The `start.sh` script runs its target with an `exec`.  This means it replaces the script instead of running as a subprocess, which means it takes over signal handling &amp; responds correctly when Docker tells it to exit.
*   Irritatingly a `sys.stdout.flush()` is required to flush the buffer and get each `print()` statement into docker-compose's output.


## Potential Improvements

*   Configurable Redis queues other than `default` - vital if we want to bring down costs by having multiple services share the same Redis
*   Authentication for Redis, particularly if the service is to be publicly exposed
*   k8s / ECS tooling for production deploys (as an alternative to docker-compose, but still utilising most of our tooling).  This should have the ability to monitor queue length and scale up the number of service-instances when it gets too long.
*   Production-quality Redis - probably using AWS ElastiCache instead of a Docker container, which gives us more resiliency
*   Monitoring, with:
    *   A simple HTTP interface built into `hw-worker` that publishes metrics (e.g. a counter for hello-worlds printed) in key=value pairs.  This will make it easy to monitor from Prometheus et al, even when the service is being scaled up &amp; down regularly by ECS or k8s.
    *   The metrics already available from Redis
    *   Prometheus to log these metrics and alert us if messages are being dropped
    *   A UI (probably Grafana) to show us the throughput of the system &amp; generate cute graphs for presentations
*   Unit tests, ideally in a form that's easy to integrate with CircleCI / Jenkins
