## Capabilities

```
$ gnmic -a router1 capabilities | awk -F  ':' '/interface/ {print $3}'
srl_nokia-if-ip, Nokia, 2023-07-31
srl_nokia-if-mpls, Nokia, 2021-06-30
srl_nokia-interfaces, Nokia, 2023-10-31
srl_nokia-interfaces-bridge-table, Nokia, 2021-06-30
srl_nokia-interfaces-bridge-table-mac-duplication-entries, Nokia, 2021-03-31
srl_nokia-interfaces-bridge-table-mac-learning-entries, Nokia, 2020-06-30
srl_nokia-interfaces-bridge-table-mac-table, Nokia, 2021-11-30
srl_nokia-interfaces-bridge-table-statistics, Nokia, 2020-06-30
srl_nokia-interfaces-ip-dhcp, Nokia, 2022-03-31
...
```

The command below to generate configurations or data from YANG models.

```
$ gnmic generate \
--dir srlinux-yang-models/ \
--file srlinux-yang-models/srl_nokia/models/interfaces/srl_nokia-interfaces.yang \
--path interface/subinterface/ipv4 \
--config-only

address:
- {}
admin-state:
- disable
allow-directed-broadcast:
- "false"
unnumbered:
  admin-state:
  - disable
  interface: []
```

The command essentially instructs `gnmic` to:

- Look into the specified directory (`srlinux-yang-models/`) for YANG models.
- Use the specified YANG model file (`srl_nokia-interfaces.yang`) to understand the data structure.
- Focus on the `ipv4` section under the `interface/subinterface` path within that YANG model.
- Generate only the configuration-related data (not the state or operational data).


```
$ gnmic generate \
--dir srlinux-yang-models/ \
--file srlinux-yang-models/ietf/ietf-ip.yang \
--path interfaces/interface/ipv4 \
--config-only
address:
- netmask: []
  prefix-length: []
enabled:
- "true"
forwarding:
- "false"
mtu: []
neighbor:
- {}
```


```
$ gnmic generate \
--dir srlinux-yang-models/ \
--file srlinux-yang-models/srl_nokia/models/interfaces/srl_nokia-interfaces.yang \
set-request \
--update interface/subinterface/ipv4

updates:
- path: interface/subinterface/ipv4
  value:
    address:
    - {}
    admin-state:
    - disable
    allow-directed-broadcast:
    - "false"
    unnumbered:
      admin-state:
      - disable
      interface: []
  encoding: JSON_IETF
```
