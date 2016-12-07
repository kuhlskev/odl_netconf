#!/usr/bin/python

import yaml
from ansible.module_utils.basic import *
from ciscoconfparse import CiscoConfParse
from re import search

IGNORED_LINES = ['no version [0-9]+\.[0-9]', 'enable secret .*', ' no key-hash ssh-rsa ', 'no interface Async', 'ip address$', 'no encapsulation slip',
                 'no license udi pid ', 'no ip route 0\.0\.0\.0 0\.0\.0\.0 ', 'no end$', '^yes$', 'do license right-to-use move securityk9',
                 'no shutdown$', '^interface\s(\w+\/)*\w*$', 'crypto key generate rsa label ', 'ip ssh pubkey-chain', '\s*exit\s*', 'snmp-server user pi pi v3 auth sha ',
                 '\s*key-string\s*', 'username mcadmin ', 'vrf definition', '!', 'address-family', 'username mcasr_', 'interface GigabitEthernet0$', 'username admin', 'username pi',
                 'service unsupported-transceiver', 'copp profile strict', 'snmp-server user pi network-operator auth sha ', 'Building configuration...', 'Current configuration : ',
                 'role priority 32667', 'vpc domain 101']
USERS = yaml.load(open('/home/vagrant/metabuilder/sshkeys.yml'))['sshkeys']

def get_mgmt_ip(file):
        mgmt_ip_regex = "(?:^\! mgmt_ip: (.*))"
        with open(file, "r") as f:
            content = f.read()
            match = re.search(mgmt_ip_regex, content, re.MULTILINE)
            if match:
                mgmt_ip = match.group(1)
                return mgmt_ip

def find_config_file(config_dir, host):
    for root, dirs, files in os.walk(config_dir):
        for file in files:
            mgmt_ip = get_mgmt_ip(os.path.join(config_dir,file))
            if mgmt_ip == host:
                return os.path.join(config_dir,file)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            device_config=dict(required=True, type='list'),
            config_dir=dict(required=True, type='str'),
            host=dict(required=True, type='str')
        ),
    )

    config_file = find_config_file(module.params['config_dir'], module.params['host'])
    if not config_file:
        module.fail_json(msg="Unable to find config file for host {}".format(module.params['host']))
    f=open(config_file)
    required_lines=f.read().split('\n')

    parse = CiscoConfParse([x.rstrip() for x in module.params['device_config']])
    diff = parse.sync_diff(required_lines,'')

    diff_lines = []
    for line in diff:
        ignored = False
        for r in IGNORED_LINES:
            if search(r, line):
                ignored = True
                break
        if not ignored:
            diff_lines.append(line)

    tmp_diff_lines = []
    for line in diff_lines:
        ignored = False
        for user, key in USERS.items():
            if search('\s*username '+user+'\s*$', line) or search('username '+user+'\s.*$', line) or search('snmp-server user '+user+'\s.*$', line):
                ignored = True
                break
        if len(line) > 100:
            ignored = True
        if not ignored:
            tmp_diff_lines.append(line)
    diff_lines = tmp_diff_lines

    if len(diff_lines) > 0:
        output_string = ""
        for line in diff_lines:
            output_string += line+"\n"
        module.fail_json(msg="Config verification failed. Required diff: \n{}".format(output_string))
    module.exit_json(changed=False)

if __name__ == '__main__':
    main()