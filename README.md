# PUMA 

Module for application migration to distributed load balance and proxy requests framework through service definition and code encapsulation.

A running instance of our framework on a migrated version of our dialog movie recommendation engine with matrix factorization is available to test at http://puma251.ddns.net:8080/ 

The code respository is located here: https://github.com/kevinjesse/puma

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Docker is a prerequisite to run PUMA and Envoy. Please install the following packages
```
$ sudo apt-get install docker, docker-compose, docker-machine
```

Now install a new machine to hold the containers
```
$ docker-machine create --driver virtualbox default
$ eval $(docker-machine env default)
```

Now clone our repository ```git clone https://github.com/kevinjesse/puma.git```

### Installing

PUMA is ready to run out of the box without needing to be built. To run, simply run ```python service.py``` in the 
```puma/envoy/examples/puma-proxy``` directory. 

### Coding Contributions
From a very high level our modifications reside in benchmark, benchmark_puma, chatbox, and envoy/puma_proxy 

Our coding contributions can be summarized in the following expanded directories. Directories not expanded do not contain PUMA modifications. 

This is a more detailed hierarchy of modified directories.
```
./puma
├── benchmark
│   └── remote_exec
│       ├── deprecated_v1
│       └── __pycache__
├── benchmark_puma
│   ├── front-proxy
│   │   └── deprecated_v1
│   └── grpc-bridge
│       ├── bin
│       ├── client
│       ├── config
│       ├── deprecated_v1
│       ├── script
│       └── service
│           ├── envoy-gen
│           ├── gen
│           ├── protos
│           └── script
├── chatbox
│   ├── backend
│   │   ├── netflix
│   │   └── resource
│   │       └── template
│   │           └── template_old
│   └── frontend
│       └── html
│           ├── css
│           └── lib
├── envoy
│   ├── bazel
│   ├── ci
│   │   └── build_container
│   ├── configs
│   │   └── original-dst-cluster
│   ├── examples
│   │   └── puma-proxy
│   │       ├── deprecated_v1
│   │       ├── migrations
│   │       │   └── versions
│   │       ├── static
│   │       │   ├── css
│   │       │   └── vendor
│   │       │       └── jquery
│   │       └── templates
│   └── include
└── tasks

```

## Running the benchmarks

Start envoy on a remote instance with ```sudo docker-compose up --build -d``` in the ```puma/benchmark/remote_exec``` directory.
On the same instance for intra-instance benchmarking, change ```puma/tasks``` to reflect the instance public or private ip. Then run 
```
python3.5 client.py
```
and the stats are printed to console. Very the parameters in client.py to change the data chunks, size of chunks, etc.


## Authors

* **Kevin Jesse** - *PUMA + Envoy + Chatbox*
* **Austin Chau** - *PUMA + Envoy + Benchmark Tests*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Lyft for Envoy Proxy framework. Super cool product
* Sam King for guidance and inspiration
