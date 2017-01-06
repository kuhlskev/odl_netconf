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

request_template_int = '''{
"lisp": {
  "mobility": {
    "dynamic-eid": {
      "dynamic-eid-name": "%s"
    }
  }
}
}'''

request_template_protocol =    '''{
  "lisp": {
"locator-set": [
      {
        "name": "campus_fabric",
        "IPv4-interface": [
          {
            "name": "%s",
            "priority": 0,
            "weight": 0
          }
        ]
      }
    ],
    "loc-reach-algorithm": {
      "rloc-probing": [
        null
      ]
    },
    "locator-table": {
      "default": [
        null
      ]
    },
    "encapsulation": {
      "vxlan": [
        null
      ]
    }
  }
}
}'''

request_template_protocol_ipv4 ='''{
    "ipv4": {
      "use-petr": [
        {
          "locator-address": "%s",
          "priority": 1,
          "weight": 1
        },
        {
          "locator-address": "%s",
          "priority": 1,
          "weight": 1
        }
      ],
      "etr": {
        "map-server": [
          {
            "ip-addr": "%s",
            "key": {
              "key-7": "%s"
            }
          },
          {
            "ip-addr": "%s",
            "key": {
              "key-7": "%s"
            }
          }
        ]
      },
      "map-cache-limit": {
        "max-map-cache-entries": 5000
      },
      "sgt": [
        null
      ],
      "itr-enable": {
        "itr": [
          null
        ]
      },
      "itr": {
        "map-resolver": [
          {
            "ip-addr": "%s"
          },
          {
            "ip-addr": "%s"
          }
        ]
      },
      "etr-enable": {
        "etr": [
          null
        ]
      }
    }
}'''

request_template_protocol_eid_table = '''{
"instance-list": [
  {
    "instance-id": %s,
    "vrf": "%s",
    "ipv4": {
      "map-cache-limit": {
        "max-map-cache-entries": 20000
      }
   }
   }
  ]
}'''

request_template_protocol_eid_table_entry = '''{          
  "dynamic-eid": [
    {
      "name": "%s",
      "database-mapping": [
        {
          "eid-prefix": "%s/24",
          "locator-set": "campus_fabric"
        }
      ]
    }
  ]
}'''
def yaml_loader(filepath):
  with open(filepath, "r") as file_descsriptor:
    data = yaml.load(file_descsriptor)
  return data

if __name__ == "__main__":
  fabric = yaml_loader("/Users/kekuhls/Documents/CIS/projects/odl_netconf/vars_files/ODL_global_fabric_vars.yml")

  request_body = request_template_protocol % (fabric['lisp']['source_int'])
  url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
    '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/router/lisp'
  #print url
  #print request_body
  print 'Adding LISP Base'
  print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))  

  request_body = request_template_protocol_ipv4 % (fabric['lisp']['locator_address'][0],fabric['lisp']['locator_address'][1], \
    fabric['lisp']['map_server'][0]['ip_address'], fabric['lisp']['map_server'][0]['key_7'], \
    fabric['lisp']['map_server'][1]['ip_address'], fabric['lisp']['map_server'][1]['key_7'], \
    fabric['lisp']['map_resolver'][0], fabric['lisp']['map_resolver'][1])

  url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
    '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/router/lisp/ipv4'
  #print url
  #print request_body
  print 'Adding LISP Base Config '
  print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))  

  for vrf in fabric['vrf']:
    request_body = request_template_protocol_eid_table % (str(vrf['vrf_id']), vrf['vrf_name'])
    url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
      '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/router/lisp/' + \
      'eid-table/instance-list/' + str(vrf['vrf_id'])
  
    #print url
    #print request_body
    print 'Adding LISP EID table for vrf ' + vrf['vrf_name']
    print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass'])) 

    for vlan in vrf['vlans']:
      request_body = request_template_protocol_eid_table_entry % (vlan['dynamic-eid-name'], vlan['ip_address'][:-1]+'0')
      url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/router/lisp/' + \
        'eid-table/instance-list/' + str(vrf['vrf_id']) + '/dynamic-eid/' + vlan['dynamic-eid-name']
      #print url
      #print request_body
      print 'Adding LISP EID entry ' + vlan['dynamic-eid-name']
      print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))         

      request_body = request_template_int % (vlan['dynamic-eid-name'])
      url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/interface/Vlan/' + \
        str(vlan['vlan_id']) + '/lisp'

      #print url
      #print request_body
      print 'Adding LISP EID to ' + vlan['name']
      print requests.put(url, data=request_body, headers=headers,auth=(fabric['odl_user'], fabric['odl_pass']))    