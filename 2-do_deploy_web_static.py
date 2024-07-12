#!/usr/bin/python3
"""
distributes an archive to my web servers
"""
from fabric.api import local, env, run, put
from os.path import isdir, exists
from datetime import datetime


env.hosts = ['34.229.189.169', '54.160.125.224']


def do_pack():
    """
    return the archive path if the archive has been correctly generated
    """
    if isdir("versions") is False:
        local("mkdir versions")
    format_date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(format_date)
    if local("tar -czvf {} web_static".format(file_name)).succeeded:
        return file_name
    else:
        return None


def do_deploy(archive_path):
    """
    deploy archive to my web servers
    """
    if exists(archive_path) is False:
        return False
    filename = archive_path.split("/")[-1]
    file_no_exts = filename.split(".")[0]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(file_no_exts))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, file_no_exts))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(file_no_exts, file_no_exts))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_no_exts))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_no_exts))
        return True
    except Exception:
        return False
