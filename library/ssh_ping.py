#!/usr/bin/env python
import pexpect
from pexpect import pxssh
from ansible.module_utils.basic import *


class SshClient(object):
    def __init__(self, module):
        self.module = module
        self.username = module.params['username']
        self.password = module.params['password']
        self.hostname = module.params['hostname']
        self.log = module.params['log']
        self.log_file = module.params['log_file']
        self.session = None
        self.logged_in = False

    def create_session(self):
        try:
            sesh = pxssh.pxssh(options={
                               "StrictHostKeyChecking": "no",
                               "UserKnownHostsFile": "/dev/null"})
            # Enable the following line if you need to see all output.
            # This will make Ansible think that there was an error, however.
            #sesh.logfile_read = sys.stdout
            if self.log:
                # To only capture output (and not passwords) change logfile to logfile_read
                sesh.logfile_read = file(self.log_file, 'w')
            sesh.force_password = True
            return sesh

        except (pxssh.ExceptionPxssh, pexpect.ExceptionPexpect) as e:
            self.module.fail_json(msg="Connection Error: {}".format(e))

    def login(self):
        try:
            # Session must be initialized before being created
            self.session = None
            sesh = self.session = self.create_session()
            sesh.login(self.hostname, self.username, self.password,
                       auto_prompt_reset=False, login_timeout=30)
            sesh.PROMPT = '\r\n.*#'
            sesh.sendline('\r\n')

            return True

        except (pxssh.ExceptionPxssh, pexpect.exceptions.TIMEOUT) as e:
            self.module.fail_json(msg="Connection Error: {}".format(e))

        except pexpect.exceptions.EOF as eof:
            self.module.fail_json(msg="Connection Error: Is {} reachable from this computer?".format(self.hostname))

def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(required=True, type='str'),
            password=dict(required=True, no_log=True, type='str'),
            hostname=dict(required=False, type='str'),
            log=dict(required=False, type='bool', default=False),
            log_file=dict(required=False, type='str', default=None),
        ),
    )
    ssh = SshClient(module)
    ssh.login()
    ssh.session.close()
    module.exit_json(changed=False)

if __name__ == '__main__':
    main()