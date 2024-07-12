#!/usr/bin/python3
"""
generates a .tgz archive from the contents of
the web_static folder of my  AirBnB_Clone repo
"""
from fabric.api import local
from os.path import isdir
from datetime import datetime


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
