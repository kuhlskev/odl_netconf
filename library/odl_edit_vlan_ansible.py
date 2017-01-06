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

headers = {'Content-Type': 'application/json'}

request_template = '''{
    "vlan-list": [
      {
        "id": %s,
        "name": %s
      }
    ]
}'''
def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            port=dict(type='int', default=8181),
            username=dict(type='str', required=True, no_log=True),
            password=dict(type='str', required=True, no_log=True),
            vlan_name=dict(type='str', required=True),
            vlan_id=dict(type='str', required=True),
            odl_server=dict(type='str', required=True),
        )
    )
    changed = False
    m_args = module.params
    request_body = request_template % (m_args['vlan_id'], m_args['vlan_name'])
    url = 'http://'+ m_args['odl_server'] + m_args['port']+'/restconf/config/network-topology:network-topology' + \
          '/topology/topology-netconf/node/' + m_args['host'] + '/yang-ext:mount/ned:native/vlan/vlan-list/' + str(m_args['vlan_id'])
  try:
    current_config = requests.get(url, headers=headers,auth=(odl_user, odl_pass))
  if json.loads(current_config) == json.loads(request_body):
    changed == False
  else:
    result = requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))
    if result.status_code != 200:
      module.fail_json(msg='Unable to add SVI entry - %s' % json.dumps(result.json(), sort_keys=True,indent=4, separators=(',', ': ')))
    changed = True
  return_msg = {}
  return_msg['changed'] = changed
  module.exit_json(**return_msg)

from ansible.module_utils.basic import *
if __name__ == "__main__":
  main() 