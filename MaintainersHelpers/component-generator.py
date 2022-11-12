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
              '<provider> <channel> <file-url> [file_path]')
        sys.exit(1)

    repository = sys.argv[1]
    maintainer = sys.argv[2]
    name = sys.argv[3]
    provider = sys.argv[4]
    channel = sys.argv[5]
    file_url = sys.argv[6]
    file_path = sys.argv[7] if len(sys.argv) > 7 else None

    if repository != 'components':
        print('only components repository is supported')
        sys.exit(1)

    if not file_url.startswith('http'):
        print('only http file urls are supported')
        sys.exit(1)

    file_name = file_url.split('/')[-1]
    if not file_path:
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
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(r.content)

    logger.info('getting file checksum and size')
    file_checksum = get_file_checksum(file_path)
    file_size = os.path.getsize(file_path)

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
            'rename': file_name,
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
