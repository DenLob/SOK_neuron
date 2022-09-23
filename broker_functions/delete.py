import os


def delete_image(tmp_img_path):
    print('Deleting image ' + tmp_img_path)
    os.remove(tmp_img_path)