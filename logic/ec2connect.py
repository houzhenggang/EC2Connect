import boto3
from .ssh import SSHConnector
from bullet import Bullet, Check


class Ec2Connect:
    def __init__(self, region='ap-northeast-1'):
        self.region = region
        self.splitter = '  '

    def list_instances(self):
        ec2 = boto3.resource('ec2', region_name=self.region)
        instance_iterator = ec2.instances.all()

        instance_list = []

        for i in instance_iterator:
            name_tag = [x['Value'] for x in i.tags if x['Key'] == 'Name']
            name = name_tag[0] if len(name_tag) else ''
            tmp = i.id + self.splitter + i.state['Name'] + self.splitter + name
            instance_list.append(tmp)

        if not instance_list:
            print('No EC2 instance in ' + self.region + '.')
            exit(127)

        print('Your EC2 Instances (' + self.region + '):')
        print()

        for i in instance_list:
            print("     " + i)

        exit(0)

    def stop_instance(self):
        ec2 = boto3.resource('ec2', region_name=self.region)
        instance_iterator = ec2.instances.all()

        instance_list = []

        for i in instance_iterator:
            name_tag = [x['Value'] for x in i.tags if x['Key'] == 'Name']
            name = name_tag[0] if len(name_tag) else ''
            tmp = i.id + self.splitter + i.state['Name'] + self.splitter + name
            instance_list.append(tmp)

        if not instance_list:
            print('No EC2 instance in ' + self.region + '.')
            exit(127)

        cli = Check(
            prompt="Hit <Space Bar> to check instances:",
            choices=instance_list,
            indent=0,
            align=3,
            margin=2,
            shift=1,
            pad_right=3,
            check='✅'
        )
        selected = cli.launch()

        for s in selected:
            id = s.split(self.splitter)[0]
            print('Stopping ' + id + '\n')

            res = ec2.Instance(id).stop()

    def start_instance(self):
        ec2 = boto3.resource('ec2', region_name=self.region)
        instance_iterator = ec2.instances.all()

        instance_list = []

        for i in instance_iterator:
            if not i.tags:
                name = ""
            else:
                name_tag = [x['Value'] for x in i.tags if x['Key'] == 'Name']
                name = name_tag[0] if len(name_tag) else ''
            tmp = i.id + self.splitter + i.state['Name'] + self.splitter + name
            instance_list.append(tmp)

        if not instance_list:
            print('No EC2 instance in ' + self.region + '.')
            exit(127)

        cli = Check(
            prompt="Hit <Space Bar> to check instances:",
            choices=instance_list,
            indent=0,
            align=3,
            margin=2,
            shift=1,
            pad_right=3,
            check='✅'
        )
        selected = cli.launch()

        for s in selected:
            instance_id = s.split(self.splitter)[0]
            print('Starting ' + instance_id + '\n')

            res = ec2.Instance(instance_id).start()

    def ssh_to_instance(self, instance_id=None):
        ec2 = boto3.resource('ec2', region_name=self.region)
        instance_iterator = ec2.instances.all()

        instance_list = []

        for i in instance_iterator:
            if (i.state['Name'] == 'running') and (i.platform != 'Windows'):
                name_tag = [x['Value'] for x in i.tags if x['Key'] == 'Name']
                name = ''
                if name_tag:
                    name = name_tag[0] if len(name_tag) else ''
                tmp = i.id + self.splitter + self.splitter + name
                instance_list.append(tmp)

        if not instance_list:
            print('No EC2 instance in ' + self.region + '.')
            exit(127)

        cli = Bullet(
            prompt="Select instance to SSH: ",
            choices=instance_list,
            indent=0,
            align=3,
            margin=2,
            shift=1,
            pad_right=3
        )
        selected = cli.launch()

        if selected:
            instance_id = selected.split(self.splitter)[0]
            instance = ec2.Instance(instance_id)

            SSHConnector.ssh_to_instance(instance.public_ip_address)
