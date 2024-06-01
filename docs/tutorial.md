# Configuration Tutorial

This tutorial will guide you through the steps of configuring Nokia srlinux routers using the gNMIc and YANG models.

The containerlab toplogy file `lab1.clab.yaml` creates the ring topology shown in the figure below:

![Topology](ring2.png)

## Stating and Stopping the Lab

To start the lab:

```
$ sudo clab deploy [-t lab1.clab.yaml]
```

To stop the lab:

```
$ sudo clab destroy [-t lab1.clab.yaml]
```

## YANG Support

SR Linux is built to support YANG data models. Therefore, all management interfaces (CLI, gNMI, and JSON-RPC) are based on a common YANG models for configuration, state, and operational tasks. For example, the CLI command tree is derived the YANG models loaded into the system and a gNMI client can use the models to configure the system.

SR Linux supports the following YANG data models:

- Nokia vendor-specific data models
- OpenConfig vendor-neutral data models

You can use the OpenConfig data models together with the SR Linux data models to configure network elements, using a CLI console or SSH connection or management-interface RPCs (gNMI) for communications between the clients and routers. The SR Linux data models offer a more complete representation of the capabilities of the SR Linux network elements, because they include vendor-specific features and functions that the OpenConfig data models do not describe.


## Configuration Tasks

This tutorial will guide you through the steps of configuring the devices in the network so that hosts will be able to communicate with each other. The configuration tasks include:

- Configuring interfaces and subinterfaces (assign IPv4 addresses).
- Configuring OSPF routing protocol.

Note that the containerlab (using the topology file) assigns names to devices and IP addresses to the hosts. It also connects all devices to a management network 172.20.20.0/24 through the devices' management interface. All configuration tasks in the tutorial are performed through the management network.

Before proceeding with this lab, please review this [Introduction to Nokia SR Linux](https://martimy.github.io/clab_srl_dcn/srlinux.html).

### Configure interfaces using CLI

Interface configuration on the srlinux router involves three steps.

1. Create a subinterface: each router interface must have at least one subinterface. If VLANs are disabled on the interface, then only one subinterface is needed.
2. Configure an IPv4 address on the subinterface
3. Enable both the parent interface and the subinterface. Also enable ipv4 address (the interface can have multiple addresses, each can be enabled individually).

Sine most people are familiar with using CLI to configure routers, this is where we will start. The srlinux was built to support YANG model from the ground up, so the CLI is based on YANG.

Use ssh to login (you can also use `docker exec -it router1 sr_cli`):

```
$ ssh admin@router1
```

Once logged in, you will be in the running mode:

```
Welcome to the srlinux CLI.
Type 'help' (and press <ENTER>) if you need any help using this.

--{ + running }--[  ]--
A:router1#
Current mode: + running
```

To make any configuration changes, you must enter the Candidate mode:

```
A:router1# enter candidate
```

Once inside the candidate mode (the bottom of the screen shows the current mode), you can update the configuration using the `set` command. Use the tab key to display a menu that shows all the next possible keywords then use the navigation keys to select the required keyword. At the end you need to type the address "192.168.1.1/24".

```
set /interface ethernet-1/21 admin-state enable subinterface 0 admin-state enable ipv4 address 192.168.1.1/24
```

Type `diff` to view the configuration changes you made.

``` {missing ipv4 enable}
A:router1# diff
+     interface ethernet-1/21 {
+         admin-state enable
+         subinterface 0 {
+             admin-state enable
+             ipv4 {
+                 address 192.168.1.1/24 {
+                 }
+             }
+         }
+     }

--{ +* candidate shared default }--[  ]--
A:router1#
```

Repeat the command using the `flat` option:

```
A:router1# diff flat
insert / interface ethernet-1/21
insert / interface ethernet-1/21 admin-state enable
insert / interface ethernet-1/21 subinterface 0
insert / interface ethernet-1/21 subinterface 0 admin-state enable
insert / interface ethernet-1/21 subinterface 0 ipv4
insert / interface ethernet-1/21 subinterface 0 ipv4 address 192.168.1.1/24

--{ +* candidate shared default }--[  ]--
A:router1#
```

These configuration changes are not committed yet, so they have no affect on the running configuration. To commit the changes, use `commit now`, which will apply the configuration and move you back to the running mode (if the configuration includes error, you will not be able to commit the changes).

```
A:router1# commit now
All changes have been committed. Leaving candidate mode.

--{ + running }--[  ]--
A:router1#
Current mode: + running
```

That was a brief demonstration of using the CLI, but this lab will focus on using gNMIc and YANG to configure the router, so exit the router by pressing `CTRL-D`, or type `quit` and press `ENTER`.

```
A:router1# quit
Connection to router1 closed.
```

### Introducing gNMIc

gNMIc is a gNMI (gRPC Network Management Interface) CLI (Command Line Interface) client and collector. It provides full support for gNMI RPCs (Remote Procedure Calls) including Capabilities, Get, Set, and Subscribe.

The gNMIc tool requires credentials and other information to be able to access routers. Instead of repeatedly supplying all of this information in the command line, we can use environment variables. So before using gNMIc, you will need to set the following environment variables:

```
export GNMIC_USERNAME=admin
export GNMIC_PASSWORD=NokiaSrl1!
export GNMIC_SKIP_VERIFY=true
export GNMIC_ENCODING=json_ietf
```

```
$ source env.sh
```

First, you can use the gNMIc's `get` command to view in the interface configuration you just created on the router:

```
$ gnmic -a router1 get --path /interface[name=ethernet-1/21]/subinterface[index=0] -t config
[
  {
    "source": "router1",
    "timestamp": 1716745564727965443,
    "time": "2024-05-26T14:46:04.727965443-03:00",
    "updates": [
      {
        "Path": "srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]",
        "values": {
          "srl_nokia-interfaces:interface/subinterface": {
            "admin-state": "enable",
            "ipv4": {
              "address": [
                {
                  "ip-prefix": "192.168.1.1/24"
                }
              ],
              "admin-state": "enable"
            }
          }
        }
      }
    ]
  }
]
```

The previous command includes the following flags:

- `-a`: Address of the target router (multiple targets can be included separated by commas).
- `--path` Specifies the path to the specific configuration data. Notice that the path includes the name of the interface and the index of the subinterface.
- `-t config`: Specifies that only configuration data is requested (this excludes statistics, for example).

The output shown above is in JSON format, which is the default. Use `flat` format to display the interface configuration in xpath-style paths:

```
$ gnmic -a router1 get --path /interface[name=ethernet-1/21]/subinterface[index=0] -t config --format flat
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/admin-state: enable
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/address.0/ip-prefix: 192.168.1.1/24
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/admin-state: enable
```

**gNMIc and XPath**

gNMIc uses YANG [XPath](xpath.md) to specify the data being requested or updated. For instance, in the previous example, the gNMIc command `get` is used to get xpaths related to the interface configuration. The `flat` format displays the configuration in path style.

It is also possible, using the gNMIc `path` command, to generate and search through the XPath-style paths extracted from a YANG file. Once paths are extracted from a YANG model, it is possible to utilize CLI search tools like `awk`, `sed` and `alike` to find the paths satisfying specific matching rules.


**Exercises:**

- Use the `get` command again but remove the interface name and the subinterface index. Describe the output.
- Why there is no IP address configured for the `mgmt0.0` interface?
  - Investigate using `$ gnmic -a router1 get --path /interface[name=mgmt0]/subinterface -t config`
  - Repeat the `get` command using the option `-t state`



### 2. Configure Interfaces using gNMI

Now we will use the gNMIc tool, instead of the CLI, to configure the interfaces on the other two routers.

To change the configuration (add, update, or delete), we need to use the `set` command. The command can be applied with several flags, including:

- `--update-path`: Specifies the path in the YANG model to the configuration item to be updated.
- `--update-value`: Provides the new value for the specified configuration item, either as a value or as a JSON object.

Since the all routers have similar configuration, we can use one command for all routers. The following command create the subinterface with index 0 (the index can be any number in the range 0 to 9999).

```
$ gnmic -a router2,router3 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0] \
--update-value '{"index": 0}'
```

The IP address for each subinterface is different so we use separate command for each router:

```
$ gnmic -a router2 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4 \
--update-value '{"address": [{"ip-prefix": "192.168.2.1/24"}]}'
$ gnmic -a router3 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4 \
--update-value '{"address": [{"ip-prefix": "192.168.3.1/24"}]}'
```

Finally, we enable all interfaces, subinterfaces, and the IPv4 addresses:

```
$ gnmic -a router2,router3 set \
--update-path /interface[name=ethernet-1/21]/admin-state \
--update-value enable \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/admin-state \
--update-value enable \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/admin-state \
--update-value enable
```

3. Create a network instance

if you try to ping from a host to one of the routers, the ping will fail:

```
$ docker exec host1 ping 192.168.1.1
```

The reason is that the subinterfaces we just configured must be associated with a network-instance (aka VRF). Initially, the only network-instance configured is the `mgmt`, in which all management interfaces belong (this instance will be ignored for now). Use the following command to verify. Note the output JSON shows that the "mgmt" network-instance has interface "mgmt0.0", which is the interface that we are using to configure the router.

```
$ gnmic -a router1 get --path /network-instance -t config
[
  {
    "source": "router1",
    "timestamp": 1716733501911687374,
    "time": "2024-05-26T11:25:01.911687374-03:00",
    "updates": [
      {
        "Path": "",
        "values": {
          "": {
            "srl_nokia-network-instance:network-instance": [
              {
                "admin-state": "enable",
                "description": "Management network instance",
                "interface": [
                  {
                    "name": "mgmt0.0"
                  }
                ],
                "name": "mgmt",
                "protocols": {
                  "srl_nokia-linux:linux": {
                    "export-neighbors": true,
                    "export-routes": true,
                    "import-routes": true
                  }
                },
                "type": "srl_nokia-network-instance:ip-vrf"
              }
            ]
          }
        }
      }
    ]
  }
]
```

We will need to create a network-instance named "default" (the "default" network-instance in srlinux has special features). The following sequence of updates create a network-instance named "default", enable it, then associate the previously configured interface.


```
$ gnmic -a router1 set \
--update-path /network-instance[name=default] \
--update-value '{"name": "default"}' \
--update-path /network-instance[name=default]/admin-state \
--update-value enable \
--update-path /network-instance[name=default] \
--update-value '{"interface": [{"name": "ethernet-1/21.0"}]}'
```


Now it is possible to ping the router from the host:

```
$ docker exec host1 ping 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=8.06 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=6.38 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=9.05 ms
...
```

For more efficiency, we you can combine all three commands using a configuration file.

Create a file `payload.json` and add the following JSON object:

```
{
  "name": "default",
  "admin-state": "enable",
  "interface": [{"name": "ethernet-1/21.0"}]
}
```

or you can use YAML in file `payload.yaml`:

```
name: default
admin-state: enable
interface:
  - name: ethernet-1/21.0
```


```
gnmic -a router2,router3 set \
--update-path /network-instance[name=default] \
--update-file payload.json
```

Let's verify ping

```
vagrant@ubuntu2004:~/myclabs/yang_lab$ docker exec host2 ping 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=64 time=18.2 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=64 time=1.59 ms
^C
vagrant@ubuntu2004:~/myclabs/yang_lab$ docker exec host3 ping 192.168.3.1
PING 192.168.3.1 (192.168.3.1) 56(84) bytes of data.
64 bytes from 192.168.3.1: icmp_seq=1 ttl=64 time=11.4 ms
64 bytes from 192.168.3.1: icmp_seq=2 ttl=64 time=5.11 ms
^C
```

Use flat format to verify configuration:

```
$ gnmic -a router2 get --path /interface[name=ethernet-1/21]/subinterface[index=0] -t config --format flat
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/admin-state: enable
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/address.0/ip-prefix: 192.168.2.1/24
srl_nokia-interfaces:interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/admin-state: enable
```

**Saving configuration**


At this point, you may be wondering how to save the configuration. You can log into teh router and save the configuration using the CLI.

```
A:router1# save startup
```

However, containerlab provides a conveinet way to save the configuration for all routers at once using the `save` command:

```
$ sudo clab save
INFO[0000] Parsing & checking topology file: lab1.clab.yaml
INFO[0004] saved SR Linux configuration from router3 node. Output:
/system:
    Saved current running configuration as initial (startup) configuration '/etc/opt/srlinux/config.json'

INFO[0004] saved SR Linux configuration from router1 node. Output:
/system:
    Saved current running configuration as initial (startup) configuration '/etc/opt/srlinux/config.json'

INFO[0004] saved SR Linux configuration from router2 node. Output:
/system:
    Saved current running configuration as initial (startup) configuration '/etc/opt/srlinux/config.json'
```

The output shows that the startup configuration is save in router's directory `/etc/opt/srlinux/config.json`. In your host machine, this file is saved under individual router's directory in the
`clab-lab1` director.

**CAUTION:** Exiting the lab using `destroy --clean-up` option, will remove the `clab-lab1`. DO NOT use this this option until after you complete the lab. Instead, you can stop the lab, if you need to, using:

```
$ sudo clab destroy
```


**More interfaces**

Now we need to configure the remaining interfaces between each pair of routers. Since now we now all the elements needed for the configuration, we can create a JSON (or YAML) file that perfrom all thress steps needed.

Edit a file `all_interfaces.yaml`:

```
interface:
- admin-state: enable
  name: ethernet-1/11
  subinterface:
    - admin-state: enable
      description: To Router2
      index: 0
      ipv4:
        admin-state: enable
        address:
          ip-prefix: 10.0.0.5/30

- admin-state: enable
  name: ethernet-1/12
  subinterface:
    - admin-state: enable
      description: To Router3
      index: 0
      ipv4:
        admin-state: enable
        address:
          ip-prefix: 10.0.0.9/30
```

Use the `set` command and the `--update-path` as before, but we now add a new flag `--update-file`, which reads the configuration from the YAML file we just created.

```
$ gnmic -a router1 set --update-path / --update-file all_interfaces.yaml
```

or

```
$ gnmic -a router1 set --update-path /interface[name=ethernet-1/11] --update-file interface_config.yaml
{
  "source": "router1",
  "timestamp": 1716849281093866469,
  "time": "2024-05-27T19:34:41.093866469-03:00",
  "results": [
    {
      "operation": "UPDATE",
      "path": "interface[name=ethernet-1/11]"
    }
  ]
}
```

Verify:

```
$ gnmic -a router1 get --path /interface -t config
```

#### Request-file


The `--request-file` flag will simplify the process even further by combining multiple paths and operations, update, replace or delete in one file.

Edite a file named `interface_req.yaml`

```yaml
updates:
  - path: /interface[name=ethernet-1/11]
    value:
      admin-state: enable
      description: router2 to router3
      subinterface:
        - index: 0
          admin-state: enable
          ipv4:
            address:
              - ip-prefix: 10.0.0.9/30
  - path: /interface[name=ethernet-1/12]
    value:
      admin-state: enable
      description: router2 to router1
      subinterface:
        - index: 0
          admin-state: enable
          ipv4:
            address:
              - ip-prefix: 10.0.0.6/30
```

Use the following `set` command for Router2.

```
$ gnmic -a router2 set --request-file interface_req.yaml
```

Edit the file for router3 and repeat



### 3. Configure OSPF


We will use the last technique to configure OSFP. The file `opsf.yaml` includes basic OSPF configuration that we can use with the command `set --request-file` to configure each router. However, we will need to assign each router a unique router-id. Instead if editing the file manually for each target router, the request-file can be written as Go Text template. The router-id values are written in separate variables file (with `_vars` added to the name):

```
updates:
{{ $target := index .Vars .TargetName }}
- path: /network-instance[name=default]/protocols/ospf
  value:
    instance:
    - name: default
      router-id: {{ index $target "router-id" }}
      version: ospf-v2
      admin-state: enable
      area:
      - area-id: 0.0.0.0
        interface:
        - admin-state: enable
          interface-name: ethernet-1/11.0
        - admin-state: enable
          interface-name: ethernet-1/12.0
        - admin-state: enable
          interface-name: ethernet-1/21.0
```

The variables file `ospf_vars.yaml`:

```
router1:
  router-id: 1.1.1.1
router2:
  router-id: 2.2.2.2
router3:
  router-id: 3.3.3.3  
```

Finally, we apply the OSPF configuration:

```
$ gnmic -a router1,router2,router3 set --request-file ospf.yaml
```

## Links

- [Nokia SR Linux 23.10 Configuration Basics](https://documentation.nokia.com/srlinux/23-10/title/basics.html)
