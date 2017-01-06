"""
Adds SVI to switch with IP address

uses HTTP PUT with JSON payload
"""
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
'''          
vrf_template = '''"vrf": {
            "forwarding": "%s"
          },'''
lisp_template ='''"lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "%s"
              }
            }
          }'''
eom = '''
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
          ip_address=dict(type='str', required=True),
          subnet_mask=dict(type='str', default='255.255.255.0'),
          vrf=dict(type='str', required=True),
          dynamic_eid_name=dict(type='str', default='None'),
          vlan_id=dict(type='str', default='None'),
          odl_server=dict(type='str', required=True),
          dhcp_server=dict(type='str', required=True),
          dhcp_source=dict(type='str', required=True),
      )
  )
  changed = False
  m_args = module.params
  request_body = request_template % (m_args['vlan_id'], m_args['dhcp_source'], m_args['dhcp_server'], m_args['subnet_mask'], m_args['ip_address'])
  if m_args['vrf_name'] is not 'None':
      request_body += vrf_template(m_args['vrf_name'])
  if m_args['dynamic-eid-name'] is not 'None':
      request_body += lisp_template(m_args['dynamic_eid_name'])
  request_body += eom
  url = 'http://'+ m_args['odl_server'] + m_args['port']+ '/restconf/config/network-topology:network-topology' + \
    '/topology/topology-netconf/node/'+ m_args['hostname'] + '/yang-ext:mount/ned:native/interface/Vlan/' + str(m_args['vlan_id'])
  try:
    current_config = requests.get(url, headers=headers,auth=(odl_user, odl_pass))
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