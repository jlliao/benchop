Benchop on Celery with Swarm
================================================

Introduction
--------------------------------------

Please go to [Benchop on Celery](https://github.com/jlliao/benchop-celery) if you would like more details of this program. This instruction would only consist of how to deploy the solution on Docker Swarm with three instances.

1. [Benchop on Celery](https://github.com/jlliao/benchop-celery)
2. [Benchop Project by Uppsala University](http://www.it.uu.se/research/scientific_computing/project/compfin/benchop)

Environments in which to use Benchop on Celery with Swarm 
--------------------------------------

- This version is used for simulating cloud environment in a single machine using docker swarm technology.
- The depolyment will take place in an OpenStack environment and require three instances. Make sure that all instances are able to communicate with each other through IP addresses. 

How to set up Benchop on Celery with Docker Swarm 
--------------------------------------

To create a swarm, ssh into our 1st instance and change its hostname. We will use this instance as the manager node.

```bash
hostname manager1
```

Contextualize the environment with `cloud-config.txt`. Then we can start a swarm by typing:

```bash
docker swarm init --advertise-addr <floating-ip-address-of-manager-node>
```

To add a working node, we need to get a token, type

```bash
docker swarm join-token worker
```

This will give us a join token, which will allow us to add a worker. An examplar outcome would be

```bash
docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    138.168.24.69:2377
```

Now, let's ssh into the 2nd instance and change its hostname. We will use it as a working node.

```bash
hostname worker1
```
Contextualize the environment with `cloud-config.txt`. After contextualization is done, copy the join token that we have gained from the manager node, paste it to the terminal of the 2nd instance. This will add the 2nd instance as a working node.

Now ssh into the 3rd instance, change its hostname. We will use it as another working node.

```bash
hostname worker2
```

Contextualize the environment with `cloud-config.txt`. After contextualization is done, copy the join token that we have gained from the manager node, paste it to the terminal of the 3nd instance. This will add the 3nd instance as another working node.

Now go back to the manager node, we first need to get our repo from GitHub.

```bash
git clone 'https://github.com/jlliao/benchop'
```

Now since our the configuration has been done with `docker-compose.yml`. The deployement configuration of Swarm is included in the `deploy` section. All we left to do is to type this line. 

```bash
cd benchop && docker stack deploy --compose-file docker-compose.yml
```

Question?
--------------------------------------

For further information on how to use Benchop on Celery, please go to [Benchop on Celery](https://github.com/jlliao/benchop-celery).