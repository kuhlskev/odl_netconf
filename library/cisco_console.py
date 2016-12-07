#!/usr/bin/env python
import pexpect
from pexpect import pxssh
from time import sleep

class ConsoleClient(object):
    def __init__(self, module):
        self.module = module
        self.console_host = module.params['console_host']
        self.con_server_user = module.params['con_server_user']
        self.con_server_pass = module.params['con_server_pass']
        self.username = module.params['device_username']
        self.password = module.params['device_password']
        self.default_user = module.params['default_user']
        self.default_pass = module.params['default_pass']
        self.console_check = module.params['console_check']
        self.device_hostname = module.params['device_hostname']
        self.virl_port = module.params['virl_port']
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
            sesh.login(self.console_host, self.con_server_user, self.con_server_pass,
                       auto_prompt_reset=False, login_timeout=90)
            sesh.PROMPT = '\r\n.*#|\r\n.*>'
            sesh.sendline('\r\n')

            if self.virl_port:
                try:
                    sesh.sendline('telnet {console_host} {virl_port}'.format(console_host=self.console_host, virl_port=self.virl_port))
                    # i = sesh.expect(["(?i)login incorrect", pexpect.TIMEOUT], timeout=1)
                    # if i == 0:
                    #     sesh.close()
                    #     self.module.fail_json(msg="Connection Error: Console login incorrect")
                    # if i == 1:
                    #     pass
                except pexpect.ExceptionPxssh as t:
                    sesh.close()
                    self.module.fail_json(msg="Connection Error: {}".format(t))

        except (pxssh.ExceptionPxssh, pexpect.exceptions.TIMEOUT) as e:
            self.module.fail_json(msg="Connection Error: {}".format(e))

        except pexpect.exceptions.EOF as eof:
            self.module.fail_json(msg="Connection Error: Is {} reachable from this computer?".format(self.console_host))

        for attempt in range(5):
            try:
                # After login, send enter to show prompt
                sesh.sendline('\r\n')
                sleep(1)
                i = sesh.expect([sesh.PROMPT, "(?i)last login", "(?i)login:", "(?i)username", "(?i)password:", "(?i)login incorrect"], timeout=30)
                if i == 0:
                    self.logged_in = True
                    sesh.sendline("terminal length 0")
                    sleep(2)
                    return True
                if i == 1:
                    # The "last login" command makes expect think it needs to send the login,
                    # so clear the expect.before buffer and try again.
                    pass
                elif i == 2 or i == 3:
                    sesh.sendline(self.username)
                    sesh.expect("(?i)password")
                    sesh.sendline(self.password)
                    pass
                elif i == 4:
                    sesh.sendline(self.password)
                    pass
                elif i == 5:
                    sesh.close()
                    self.module.fail_json(msg="Connection Error: Device username/password incorrect")

            # If the login fails, catch the exception and retry again
            except (pxssh.ExceptionPxssh, pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as e:
                pass

        # If all retries fail, error out
        else:
            sesh.close()
            self.module.fail_json(msg="Login Error: {}".format(e))

    def check_hostname(self):
        sesh = self.session
        sesh.sendline('\r\n')
        i = sesh.expect([self.device_hostname, pexpect.TIMEOUT], timeout=5)
        if i == 0:
            return True
        if i == 1:
            lines = sesh.before.split()
            hostname = lines[-1].strip('#')
            self.disconnect()
            self.module.fail_json(msg="Login Error: Expected device '{}'. Got device: '{}' connected to console.".format(self.device_hostname, hostname))
        # Need to run readline() twice to get to the line with the hostname
        # command = sesh.readline()
        # hostname = sesh.readline()
        # line3 = sesh.readline()
        # line4 = sesh.readline()
        # line5 = sesh.readline()
        # line6 = sesh.readline()
        # elif i == 1 or i == 2:
        #     #lines = sesh.after.split('\r')


    def version(self):
        sesh = self.session
        sesh.sendline('show version')
        sesh.expect('Configuration register')
        return sesh.before

    def disconnect(self):
        # Cannot use logout() since this is a console. Manually disconnect
        self.session.sendline('exit')
        self.session.close()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            console_host=dict(required=True, type='str'),
            con_server_user=dict(required=True, type='str'),
            con_server_pass=dict(required=True, no_log=True, type='str'),
            device_username=dict(required=True, type='str'),
            device_password=dict(required=True, no_log=True, type='str'),
            default_user=dict(required=False, type='str', default='admin'),
            default_pass=dict(required=False, no_log=True, type='str', default='admin'),
            virl_port=dict(required=False, type='str', default=None),
            log=dict(required=False, type='bool', default=False),
            log_file=dict(required=False, type='str', default=None),
            console_check=dict(required=False, type='bool', default=False),
            device_hostname = dict(required=False, type='str'),
        ),
        required_together = [
            ['console_check', 'device_hostname']
        ]
    )
    con = ConsoleClient(module)
    con.login()
    if con.console_check:
        con.check_hostname()
        con.disconnect()
        module.exit_json(changed=False, console_access=True)
    con.disconnect()
    module.exit_json(changed=False)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()