# XPATH

YANG organizes the data models into hierarchy of modules and submodules. The following is a simple YANG model for a network interface:

```yang
module example-interface {
    namespace "http://example.com/ns/interfaces";
    prefix "if";

    container interfaces {
        list interface {
            key "name";
            leaf name {
                type string;
            }
            leaf description {
                type string;
            }
            leaf enabled {
                type boolean;
            }
        }
    }
}
```

While YANG models describe the data, the YANG data instances are represented in XML or JSON formats. In an XML representation, the data describing two interfaces looks like the following:

```xml
<interfaces xmlns="http://example.com/ns/interfaces">
    <interface>
        <name>eth0</name>
        <description>Main interface</description>
        <enabled>true</enabled>
    </interface>
    <interface>
        <name>eth1</name>
        <description>Backup interface</description>
        <enabled>false</enabled>
    </interface>
</interfaces>
```

XPath (XML Path Language) is an expression language that uses "path-like" syntax to identify and navigate through elements and attributes in an XML document. XPath is used within YANG data models to define constraints on the elements of a YANG data model. It also allows for the selection of specific nodes in the data tree based on certain criteria.

XPath works with YANG in the following ways:

1. An XPath expression can be used to query and retrieve a specific configuration element from an XML data structure defined by a YANG model.
2. An XPath can be used to specify the conditions that a particular element in the YANG model must meet, such as matching a certain pattern or falling within a certain range.
3. XPath expressions can be used (by NETCONF, for example) to select specific parts of the configuration or state data during network operations. For instance, a NETCONF \<get\> operation might use an XPath expression to filter the data retrieved from a network device.

An XPath expression to select the description of the interface named "eth0" from the previous example would be:

```
/interfaces/interface[name='eth0']/description
```
