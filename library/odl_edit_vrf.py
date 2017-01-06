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
  "definition": [
    {
      "name": "%s",
      "address-family": {
        "ipv4": {
          "route-target": {
            "export": [
              {
                "asn-ip": "%s"
              }
            ],
            "import": [
              {
                "asn-ip": "%s"
              }
            ]
          }
        }
      },
      "rd": "%s"
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
      vrf_id = str(vrf['vrf_id']) +':'+ str(vrf['vrf_id'])
      request_body = request_template % (vrf['vrf_name'], vrf_id, vrf_id, vrf_id)
      url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/vrf/definition/' + vrf['vrf_name']
      print url
      print request_body
      print 'Adding Vrf ' + vrf['vrf_name']
      print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))    