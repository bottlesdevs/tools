import os
import sys
import yaml
import requests
import hashlib
import shutil
from glob import glob
from pathlib import Path


ignored_files = ["index.yml", "testing.yml"]
temp_path = f"{Path.home()}/__temp__"
progressbar_sym = "|/-\\"
show_progress=False if os.environ.get("HIDE_PROGRESS") else True


def clean_temp_path():
    shutil.rmtree(temp_path)


def check_temp_path():
    '''Checks if the temp path exists, if not, creates it'''
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)


def get_file_checksum(file_path):
    '''Returns the MD5 checksum of a file'''
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def progress_bar(title, count, block_size, total_size):
    '''Prints a progress bar'''
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write(f"\r{progressbar_sym[count % 4]} {title} {percent}%")
    sys.stdout.flush()


def download_file(url):
    '''Downloads a file to __temp__ and returns its path'''
    file_name = url.split('/')[-1]
    file_path = f"{temp_path}/{file_name}"
    try:
        response = requests.get(url, stream=True)
    except requests.exceptions.MissingSchema as e:
        print(f"\n[ERROR] | {file_name}: {e}")
        return False
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    count = 0

    if total_size != 0:
        with open(file_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                count += 1
                if show_progress:
                    progress_bar(file_name, count, block_size, total_size)
        return file_path
    else:
        print(f"\n[ERROR] | {file_name}: File size is 0")
        return False


def update_checksum(file_path, file_name, checksum):
    '''Update manifest checksum'''
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    step = [step for step in data['Steps'] if step.get('file_name') and step['file_name'] == file_name][0]
    step['file_checksum'] = checksum
    with open(file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def update_size(file_path, file_name, file_size):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    step = [step for step in data['Steps'] if step.get('file_name') and step['file_name'] == file_name][0]
    step['file_size'] = file_size
    with open(file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def process_manifest(manifest):      
    '''Processes a manifest'''
    with open(manifest, 'r') as f:
        data = yaml.safe_load(f)
    
    name = data["Name"]
    for step in data['Steps']:
        if 'file_checksum' in step and "file_name" in step:
            url = step['url']
            if url.startswith("temp"):
                continue
            file_name = step['file_name']
            file_path = download_file(url)
            if not file_path:
                continue
            checksum = get_file_checksum(file_path)
            file_size = os.path.getsize(file_path)

            if checksum != step['file_checksum']:
                print(
                    f"\n[HASH_MISMATCH] | {name}", 
                    f"---> (updating) | {name}: {checksum} -> {step['file_checksum']}", 
                    sep="\n\t"
                )
                update_checksum(manifest, file_name, checksum)

            if file_size != step['file_size']:
                print(
                    f"\n[SIZE_MISMATCH] | {name}", 
                    f"---> (updating) | {name}: {file_size} -> {step['file_size']}", 
                    sep="\n\t"
                )
                update_size(manifest, file_name, file_size)

            os.remove(file_path)


def main():
    check_temp_path()
    if len(sys.argv) < 2:
        print("Please provide a path")
        sys.exit(0)
    
    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        sys.exit(0)
    
    manifests = glob(f"{path}/**/*.yml", recursive=True)
    valid_manifests = []
    
    for i, manifest in enumerate(manifests):
        if not any(f in manifest for f in ignored_files):
            valid_manifests.append(manifest)

    print(
        f"\nFound {len(valid_manifests)} manifests",
        "-------------------------------------------------------",
        sep="\n"
    )

    for v in valid_manifests:
        process_manifest(v)

    clean_temp_path()


if __name__ == "__main__":
    main()
