import os
from fabric.api import *

HOST="192.168.1.102"
COMMAND="uname -a"

env.user = os.getenv('SSH_USER', 'vagrant')
env.password = os.getenv('SSH_PASSWORD', 'vagrant')

@hosts(HOST)
def do_something():
    run(COMMAND)