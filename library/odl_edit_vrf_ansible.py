"""
put-node.

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

import requests, json

def main():
  module = AnsibleModule(
      argument_spec=dict(
          host=dict(type='str', required=True),
          port=dict(type='int', default=8181),
          odl_user=dict(type='str', required=True, no_log=True),
          odl_password=dict(type='str', required=True, no_log=True),
          vrf=dict(type='str', required=True),
          odl_server=dict(type='str', required=True),
          rd=dict(type='str', required=True),
          rt_export=dict(type='str', required=True),
          rt_import=dict(type='str', required=True),
      )
  )
  #need logic for list of rt import/export
  changed = False
  m_args = module.params
  request_body = request_template % (m_args['vrf'], m_args['rt_export'], m_args['rt_import'], m_args['rd'])
  url = 'http://'+ m_args['odl_server'] + ':' + str(m_args['port'])+ '/restconf/config/network-topology:network-topology' + \
    '/topology/topology-netconf/node/' + m_args['host'] + '/yang-ext:mount/ned:native/vrf/definition/' + m_args['vrf']
#try
  current_config = requests.get(url, headers=headers,auth=(m_args['odl_user'], m_args['odl_password']))
#except
  #module.fail_json(msg='Current - %s' % json.dumps(current_config.json(), sort_keys=True,indent=4, separators=(',', ': ')))
  if json.loads(current_config) == json.loads(request_body):
    changed = False
  else:
    result = requests.put(url, data=request_body, headers=headers,auth=(m_arg['odl_user'], m_args['odl_pass']))
    if result.status_code != 200:
      module.fail_json(msg='Unable to add SVI entry - %s' % json.dumps(result.json(), sort_keys=True,indent=4, separators=(',', ': ')))
    changed = True
  return_msg = {}
  return_msg['changed'] = changed
  module.exit_json(**return_msg)

from ansible.module_utils.basic import *
if __name__ == "__main__":
  main()   