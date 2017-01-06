"""
put-node.

adds a node to ODL

parameter:
* ODL IP address
* node IP address
* node name
* netconf port (optional - default is 830)
* netconf user (optional - default is 'cisco')
* netconf pass (optional - default is 'cisco')

uses HTTP PUT with JSON payload
"""

import requests
import yaml

headers = {'Content-Type': 'application/json'}

request_template = '''{
      "Vlan": [
        {
          "name": "%s",
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "%s"
              }
            },
            "helper-address": [
              {
                "address": "%s",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "%s",
                "address": "%s"
              }
            }
          },
          "vrf": {
            "forwarding": "%s"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "%s"
              }
            }
          }
        }
    ]
}'''

def yaml_loader(filepath):
  with open(filepath, "r") as file_descsriptor:
    data = yaml.load(file_descsriptor)
  return data

if __name__ == "__main__":
  fabric = yaml_loader("/Users/kekuhls/Documents/CIS/projects/odl_netconf/vars_files/ODL_global_fabric_vars.yml")
  for vrf in fabric['vrf']:
    for vlan in vrf['vlans']:
      request_body = request_template % (vlan['vlan_id'], fabric['dhcp_source'], fabric['dhcp_server'], vlan['subnet_mask'], vlan['ip_address'], vrf['vrf_name'], vlan['dynamic-eid-name'])
      url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/'+ fabric['node'] + '/yang-ext:mount/ned:native/interface/Vlan/' + str(vlan['vlan_id'])
      print url
      print request_body
      print 'Adding SVI ' + str(vlan['vlan_id'])
      print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))    