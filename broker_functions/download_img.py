import os

import cv2
import paramiko

from broker_functions.delete import delete_image
from logger_funcs import color_logger


def download_img(hostname, myuser, remotepath, tmp_dir):
    mySSHK = './keys/main_server_key'
    sshcon = paramiko.SSHClient()  # will create the object
    sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # no known_hosts error
    sshcon.connect(hostname, username=myuser, key_filename=mySSHK)  # no passwd needed

    sftp = sshcon.open_sftp()
    localpath = tmp_dir + os.path.basename(remotepath)
    print("Downloading image", remotepath)
    sftp.get(remotepath, localpath)
    sftp.close()
    sshcon.close()
    color_logger.out_green("Image " + remotepath + " downloaded!")
    img = cv2.imread(localpath)
    if img is None:
        delete_image(localpath)
        return False
    return localpath
