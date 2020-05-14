There are many benchmarks comparing different languages and platforms performance to each other, but not all of them are doing this right. It's easy to find benchmarks comparing Golang working on all cores with node.js started in a single process. Or utilising DB connection pools in one language/framework and not doing it in another.

The goal of this project is to write simple and fare(-ish) benchmarks for a smaller set of languages I understand how to use efficiently and demonstrate that the difference in performance may not be that dramatic (how it is sometimes shown on the internet). No fine tuning is done to run each language/server at a maximum possible speed, rather they all run at default settings and use easily available features of their platforms.

## Notes

- Go can handle I/O in non-blocking fashion and schedule blocking operations to be run in parallel on different cores. node.js is using `libuv` for executing I/O operations asynchronously in a single threaded event loop. Python can run blocking I/O operations on threads or utilize its `asyncio` module similar to node.js approach. Both node.js and Python web servers should be run in several processes to handle CPU-bound tasks more efficiently.
- node.js is utilizing all available cores with `cluster` module or `pm2` cluster mode. node.js is handling I/O asynchronously by default with `libuv` under the hood.
- For the Python synchronous server variant I picked `gunicorn` (workers and threads are set to a number of cores available on the system).
- For the asynchronous Python server `uvicorn` is used with workers utilizing all CPU cores as well. I also test with two different event loop implementations: default `asyncio` loop and `uvloop`.
- Golang is scaling itself on all cores by default since Go 1.5, explicit `GOMAXPROCS` setting is used for clarity.
- PostgreSQL 12.2 is used as a database containing the same generated data set for all benchmarks. Servers connect to the database using connection pools (maxed at 100 connections) provided by DB libraries.
- Absolute results obtained don't matter and will vary a lot depending on your workload, this bench is about relative performance for the similar workload.
- For running the benchmarks I chose Apache HTTP server benchmarking tool (`ab`) because of its handling of TCP connections being more [realistic](http://gwan.com/en_apachebench_httperf.html) comparing to `wrk`.
- By default `net.core.somaxconn` in Linux is set to 128, so all the tests are running at a concurrency level of 128 (`ab -c` option).
- HTTP requests logging is always disabled.

## Workload

All benchmarks maintain a similar workload across languages, which includes:

- Handling HTTP requests and pooled database connections.
- CPU bound operations (e.g. serializing JSON, parsing HTTP headers).
- Memory allocation and garbage collection (e.g. creating DTO-like structures for each row in the database and discarding them).

Basically, each benchmark is running on all cores with a database connection pool(s) and on each request it simply fetches a 1000 fake users from the database, creates a class instance/structure for each row converting a datetime object to ISO string, serializes resulting array to JSON and responds with this payload. This gives near-100% CPU utilization for all languages used.

## Running servers and benchmarks

Run `make` once in the root dir to prepare the DB and `make db-clear` to remove created Docker container and associated volume.

### Servers

Golang:
- `cd golang`
- `export $(cat ../.makerc | xargs) && GOMAXPROCS=$(nproc) go run http/main.go`

node.js:
- `cd nodejs`
- `export $(cat ../.makerc | xargs) && node cluster-http.js`
- `export $(cat ../.makerc | xargs) && pm2 start pm2-http.js --instances max`

Python:
- `cd python`
- `python -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `export $(cat ../.makerc | xargs) && gunicorn --workers $(nproc) --threads $(nproc) --log-level warning gunicorn-bare:app`
- `export $(cat ../.makerc | xargs) && uvicorn --workers $(nproc) --loop asyncio --log-level warning uvicorn-bare:app`
- `export $(cat ../.makerc | xargs) && uvicorn --workers $(nproc) --loop uvloop --log-level warning uvicorn-bare:app`

### Benchmark

`ab -n 10000 -c 128 http://localhost:8000/`

## Results

### Specs

Tests were executed on a virtual machine running Ubuntu 19.10 in VirtualBox:

- CPU: AMD Ryzen 5 2600 (6 out of 12 cores available to the VM)
- RAM: Corsair CMW16GX4M2C3000C15 DDR4-3000 16gb (8gb available to the VM)
- SSD: Samsung SSD 970 EVO Plus

| Language/platform | Server/framework | Requests per second  | Time per request (ms) |
| ----------------- | ---------------- | --------------------:| ---------------------:|
| Golang 1.14       | net/http         | 1218                 | 0.821                 |
| node.js 14        | cluster, http    | 745                  | 1.341                 |
| node.js 14        | pm2, http        | 728                  | 1.373                 |
| Python 3.8        | gunicorn         | 379                  | 2.632                 |
| Python 3.8        | uvicorn/asyncio  | 874                  | 1.143                 |
| Python 3.8        | uvicorn/uvloop   | 915                  | 1.092                 |
