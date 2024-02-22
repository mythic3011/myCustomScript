import os
import hashlib
import collections
from concurrent.futures import ThreadPoolExecutor


def calculate_sha256(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def find_duplicates(dir_path):
    file_hashes = collections.defaultdict(list)
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for dirpath, dirnames, filenames in os.walk(dir_path):
            file_paths = [os.path.abspath(os.path.join(dirpath, filename))
                          for filename in filenames]
            results = executor.map(calculate_sha256, file_paths)
            for file_path, file_hash in zip(file_paths, results):
                file_hashes[file_hash].append(file_path)
    return {k: v for k, v in file_hashes.items() if len(v) > 1}


def delete_duplicates(duplicates, batch_delete=False):
    for file_paths in duplicates.values():
        sorted_paths = sorted(file_paths, key=os.path.getmtime)
        for i in range(len(sorted_paths) - 1):
            print(f"Duplicate files: {sorted_paths}")
            if batch_delete:
                to_delete = sorted_paths[i]
            else:
                response = input("Delete old one (o) or new one (n)? ")
                if response.lower() == 'o':
                    to_delete = sorted_paths[i]
                elif response.lower() == 'n':
                    to_delete = sorted_paths[i + 1]
                else:
                    print("Invalid response. Skipping these files.")
                    break
            print(f"Deleting file: {to_delete}")
            os.remove(to_delete)


# current directory
dir_path = os.path.abspath(os.getcwd())
duplicates = find_duplicates(dir_path)
for file_hash, file_paths in duplicates.items():
    abs_paths = [os.path.abspath(p) for p in file_paths]
    print(f"Hash: {file_hash}, Files: {file_paths}")

batch_delete = input("Batch delete all duplicates (y/n)? ").lower() == 'y'
delete_duplicates(duplicates, batch_delete)
