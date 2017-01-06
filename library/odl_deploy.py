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

import sys
import os
import requests
import yaml

vlan_url = "http://{{ODL_SERVER}}:8181/restconf/config/network-topology:network-topology" + \
        "/topology/topology-netconf/node/{{node}}/yang-ext:mount/ned:native/vlan/vlan-list/{{vlan_id}}"

svi_url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/'+ fabric['node'] + '/yang-ext:mount/ned:native/interface/Vlan/' + str(vlan['vlan_id'])        

def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            port=dict(type='int', default=8181),
            username=dict(type='str', required=True, no_log=True),
            password=dict(type='str', required=True, no_log=True),
            payload=dict(type='str', required=True),
            url=dict(type='str', required=True),
            node=dict(type='str', required=True),
        )
    )

    odlkwargs = dict(
        host=module.params['host'],
        port=module.params['port'],
        username=module.params['username'],
        password=module.params['password'],
    )
    retkwargs = dict()

    try:
        requests.get(url, data=request_body, headers=headers,auth=(odl_user, odl_pass)) 
    except ncclient.transport.errors.AuthenticationError:
        module.fail_json(
            msg='authentication failed while connecting to device'
        )
    except:
        e = get_exception()
        module.fail_json(
            msg='error connecting to the device: ' +
                str(e)
        )
        return
    #compare return to the about to be sent data


    retkwargs['server_capabilities'] = list(m.server_capabilities)
    try:
        changed = equests.get(
            url, 
            data=request_body, 
            headers=headers,
            auth=(odl_user, odl_pass) 
        )

    module.exit_json(changed=changed, **retkwargs)


# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()




# vlan_id: 
# vlan_name: 
request_template = '''{
    "vlan-list": [
      {
        "id": %s,
        "name": %s
      }
    ]
}'''

def yaml_loader(filepath):
  with open(filepath, "r") as file_descsriptor:
    data = yaml.load(file_descsriptor)
  return data

print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass)) 

if __name__ == "__main__":
  fabric = yaml_loader("/Users/kekuhls/Documents/CIS/projects/odl_netconf/vars_files/ODL_global_fabric_vars.yml")
  for vrf in fabric['vrf']:
    for vlan in vrf['vlans']:
      request_body = request_template % (vlan['vlan_id'], vlan['name'])
      url = 'http://'+ fabric['ODL_SERVER'] + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/' + fabric['node'] + '/yang-ext:mount/ned:native/vlan/vlan-list/' + str(vlan['vlan_id'])
      print url
      print request_body
      print 'Adding Vlan ' + str(vlan['vlan_id'])
      print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))    