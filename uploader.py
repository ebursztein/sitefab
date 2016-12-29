from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists

import files


def deploy(local_dir, remote_dir, web_user):
    # Create a directory on a remote server, if it doesn't already exists
    if not exists(remote_dir):
        run('mkdir -p '+ remote_dir)

    # Sync the remote directory with the current project directory.
    rsync_project(local_dir=local_dir, remote_dir=remote_dir, exclude=['.git'])

    # Chown an chmod
    cmd = "chown -R %s %s" % (web_user, remote_dir)
    run(cmd)
    cmd = "chmod -R 755 %s" % (remote_dir)
    run(cmd)

    # Restart the nginx server
    run('nginx -s reload')


site = files.load_config("../configuration/site_vars.yaml") #FIXME make it a command line argument
config = files.load_config("../configuration/generator_config.yaml") #FIXME make it a command line argumen


env.host_string = site.ip
env.user = 'root'
env.key_filename = site.ssh_key
remote_dir = site.remote_dir.dev #FIXME command line switch
deploy(config.dir.output, remote_dir, site.remote_user)