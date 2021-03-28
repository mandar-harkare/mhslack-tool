#!/usr/bin/python3
import sys
import os
import yaml
import paramiko
from scp import SCPClient

ssh = paramiko.SSHClient()

def getYMLContents(filename=''):
    with open(r'./configurations/'+filename+'.yml') as file:
        return yaml.full_load(file)


def getServers():
    servers = []
    ymlData = getYMLContents('servers')
    for item, doc in ymlData.items():
        if (item == 'servers'):
            servers = doc
    return servers


def getCommands(type='configure', appendCustomCommands=True):
    commands = ['sudo apt-get update']
    ymlData = getYMLContents('packages')
    if type == 'configure' or type == 'install':
        for package in ymlData['add']:
            if package:
                commands.append('sudo apt-get install ' + package + ' -y')
    elif type == 'remove':
        for package in ymlData['remove']:
            if package:
                commands.append('sudo apt-get remove ' + package + ' -y')
    if appendCustomCommands:
        ymlData = getYMLContents('servers')
        commands += ymlData['commands']
    
    return commands


def getServices(type='start'):
    commands = []
    ymlData = getYMLContents('services')
    if type == 'start':
        for service in ymlData['start']:
            if service:
                commands.append('sudo systemctl start ' + service)
                commands.append('sudo systemctl enable ' + service)
    elif type == 'stop':
        for service in ymlData['stop']:
            if service:
                commands.append('sudo systemctl stop ' + service)
    elif type == 'restart':
        for service in ymlData['restart']:
            if service:
                commands.append('sudo systemctl restart ' + service)
    
    return commands


def install(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getCommands()
    
    for server in servers:
        print('Installing packages on server: ' + server)
        # execute the commands
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(err)


def remove(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getCommands('remove', False)
    
    for server in servers:
        print('Removing packages from server: ' + server)
        # execute the commands
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(err)


def start(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getServices()
    
    for server in servers:
        print('Starting services on server: ' + server)
        # execute the commands
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(err)


def stop(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getServices('stop')
    
    for server in servers:
        print('Stoppinig services on server: ' + server)
        # execute the commands
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(err)


def restart(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getServices('restart')
    
    for server in servers:
        print('Restarting services on server: ' + server)
        # execute the commands
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(err)

def deployFile(servers=[]):
    if not servers:
        servers = getServers()
    
    commands = getServices('restart')
    
    for server in servers:
        print('Deploying index file on server: ' + server)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=os.environ.get('username'), password=os.environ.get('password'))
        
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.put('./www/index.php', '/tmp/index.php')

def configure():
    deployFile()
    install()
    start()


def help():
    text = """
    Example usage: mhslack configure | install | remove | start | stop | restart | help
    configure: Configure all the provided servers with the mentioned packages and services
    install: Install all the mentioned packages on all the servers  
    remove: Remove all the mentioned packages from all the servers  
    start: Start all the mentioned services on all the servers  
    stop: Stop all the mentioned services on all the servers  
    restart: Restart all the mentioned services on all the servers  
    help: Example usage  
    """
    print (text)


def main(argv):
    try:
        print('Hello World')
        print (argv[0])
        # result = getattr(argv[0], 'bar')()
        return eval(argv[0] + "()")
    except Exception as e:
        text = str(e)
        text += """
        Something went wrong!
        Run `mhslack help` for example usage.
        """
        print (str(text))
        sys.exit(2)
    

if __name__ == "__main__":
   main(sys.argv[1:])
