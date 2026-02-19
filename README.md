# Model-Driven Network Managment with gNMIc and YANG

The objective of this lab is to configure Nokia SR Linux routers using gNMIc interface and YANG models.

## How to Navigate and Use This Repo

1. Start with the tutorial: Your main guide is the tutorial in [docs/tutorial.md]. It will walk you through the entire process.
2. Meet the prerequisites: Ensure you have a Linux machine with Docker, Containerlab, and gNMIc installed, as noted below.
3. Clone and launch: Clone the repository and use the `lab1.clab.yaml` file with `containerlab deploy` to spin up the virtual network.
4. Follow the steps: The tutorial will guide you to run gNMIc commands to configure the routers using YANG models.
5. Experiment: Once the lab is running, you can explore the `config/` directory or modify the scripts to try your own configurations.

## Background

To use this lab, you must be familiar with the following:

- [Docker](https://www.docker.com/)
- [Containerlab](https://containerlab.dev/)
- [Nokia SR Linux](https://www.nokia.com/networks/ip-networks/service-router-linux-NOS/)
- [YANG](https://datatracker.ietf.org/doc/html/rfc7950)
- [gNMI](https://github.com/openconfig/gnmi)
- [gNMIc](https://gnmic.openconfig.net/)

## Installation

To proceed with the lab, you will need a Linux VM. You also need to install the following:

- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [Containerlab](https://containerlab.dev/install/)
- [gNMIc](https://gnmic.openconfig.net/install/)

Clone this lab to a directory in your machine:

```
$ git clone https://github.com/martimy/clab_yang [folder name]
```

## Configuration

Follow the instructions in this [tutorial](docs/tutorial.md) to start lab and configure the routers.

## Links

- [Nokia SR Linux 23.10 Configuration Basics](https://documentation.nokia.com/srlinux/23-10/title/basics.html)

## Author

Created by Maen Artimy - [Personal Blog](http://adhocnode.com)

