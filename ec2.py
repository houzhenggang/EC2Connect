import fire
from logic.ec2connect import Ec2Connect


class EC2:
    def __init__(self, region='ap-northeast-1'):
        self.ec2_connect = Ec2Connect(region)

    def list(self):
        return self.ec2_connect.list_instances()

    def stop(self):
        return self.ec2_connect.stop_instance()

    def start(self):
        return self.ec2_connect.start_instance()

    def ssh(self):
        return self.ec2_connect.ssh_to_instance()


def entry():
    fire.Fire(EC2)


if __name__ == "__main__":
    fire.Fire(EC2)
