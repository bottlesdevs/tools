'''create a program with arguments:
-repository: components (currently the only supported)
-maintainer: the maintainer name (your name)
-name: the component name
-provider: the provider name
-channel: the channel name (e.g. stable, unstable)
-file-url: the direct http url to the component file
-rename: the new name for the component (optional)
the program create a folder with name _tmp in the current directory
then downlaod the file-url to the _tmp folder and get its MD5 hash
and save its file size
get the component name from the file name
if rename is specificed, the file name will be the new name
then create a new yaml file with the following format:
---
Name: <component name>
Provider: <provider name>
Channel: <channel name>
File:
 - file_name: <file name>
   url: <file url>
   file_checksum: <file md5 hash>
   file_size: <file size>
   rename: <new name> (only if rename is specified)
and save the yaml file in the current directory.

Note: use logging module to log the output of the program
'''


import logging
import hashlib
import os
import sys
import yaml
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 4:
        print('usage: component-generator.py <repository> <maintainer> <name> '
              '<provider> <channel> <file-url> [rename]')
        sys.exit(1)

    repository = sys.argv[1]
    maintainer = sys.argv[2]
    name = sys.argv[3]
    provider = sys.argv[4]
    channel = sys.argv[5]
    file_url = sys.argv[6]
    rename = sys.argv[7] if len(sys.argv) > 7 else None

    if repository != 'components':
        print('only components repository is supported')
        sys.exit(1)

    if not file_url.startswith('http'):
        print('only http file urls are supported')
        sys.exit(1)

    logger.info('creating temp directory')
    temp_dir = os.path.join('_tmp')
    if not os.path.exists('_tmp'):
        os.makedirs(temp_dir)

    logger.info('downloading file')
    r = requests.get(file_url, allow_redirects=True)
    if r.status_code != 200:
        print('failed to download file')
        sys.exit(1)

    logger.info('saving file')
    file_name = file_url.split('/')[-1]
    with open(os.path.join(temp_dir, file_name), 'wb') as f:
        f.write(r.content)

    logger.info('getting file checksum and size')
    file_checksum = get_file_checksum(os.path.join(temp_dir, file_name))
    file_size = os.path.getsize(os.path.join(temp_dir, file_name))

    logger.info('creating yaml file')
    yaml_file = {
        'Name': name,
        'Provider': provider,
        'Maintainer': maintainer,
        'Channel': channel,
        'File': [{
            'file_name': file_name,
            'url': file_url,
            'file_checksum': file_checksum,
            'file_size': file_size,
            'rename': rename if rename else file_name
        }]
    }
    
    logger.info('saving yaml file')
    with open(os.path.join('.', name + '.yml'), 'w') as f:
        yaml.dump(yaml_file, f, default_flow_style=False, sort_keys=False)


def get_file_checksum(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)

        return md5.hexdigest()


if __name__ == '__main__':
    main()
