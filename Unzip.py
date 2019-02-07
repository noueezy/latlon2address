
import zipfile
import glob
import os

def unzip(dl_path):

    search_query = dl_path + '/*.zip'

    zip_list = glob.glob(search_query)

    for path in zip_list:
        with zipfile.ZipFile(path) as existing_zip:
            existing_zip.extractall(dl_path)

if __name__ == '__main__':
    dl_path = os.getcwd() + '/data'
    unzip(dl_path)
