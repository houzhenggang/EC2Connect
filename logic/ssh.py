import subprocess


class SSHConnector:
    def __init__(self):
        pass

    @staticmethod
    def ssh_to_instance(host):
        res = subprocess.call(['ssh', 'ec2-user@' + host])
        print(res)
