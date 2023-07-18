import os
import argparse
import hashlib

__author__ = "Matthew J. Harmon"
__license__ = "MIT"

KEY = b'SmurfsAreProtoHobbits'

def generate_hash(file_path):
    hasher = hashlib.blake2sp(digest_size=16, key=KEY)
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def generate_hashes(directory, output_file):
    with open(output_file, 'w') as file:
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_hash = generate_hash(file_path)
                file_entry = f'{file_path}: {file_hash}\n'
                file.write(file_entry)
                print(file_entry.strip())

def verify_hashes(directory, hash_file, output_failed_file):
    failed_files = []
    with open(hash_file, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                file_path, expected_hash = map(str.strip, parts)
                computed_hash = generate_hash(file_path)
                if expected_hash == computed_hash:
                    print(f'{file_path}: Hash verified')
                else:
                    print(f'{file_path}: Hash verification failed')
                    failed_files.append(file_path)

    if failed_files:
        with open(output_failed_file, 'w') as failed_file:
            for file_path in failed_files:
                failed_file.write(file_path + '\n')
        print(f'Failed verification files saved to: {output_failed_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate and verify hashes using the Blake2sp algorithm with a custom key')
    parser.add_argument('directory', metavar='DIRECTORY', help='path to the directory')
    parser.add_argument('--generate', action='store_true', help='generate hashes for files')
    parser.add_argument('--verify', action='store_true', help='verify hashes for files')
    parser.add_argument('--output', metavar='OUTPUT_FILE', default='hashes.txt',
                        help='output file to save generated hashes (default: hashes.txt)')
    parser.add_argument('--hashfile', metavar='HASH_FILE',
                        help='file containing previously generated hashes for verification')
    parser.add_argument('--failedfile', metavar='FAILED_FILE', default='failed_verification.txt',
                        help='output file to save failed verification files (default: failed_verification.txt)')

    args = parser.parse_args()

    if not args.generate and not args.verify:
        parser.error('Please specify either --generate or --verify')

    if args.generate:
        generate_hashes(args.directory, args.output)

    if args.verify:
        if not args.hashfile:
            parser.error('Please specify --hashfile for verification')
        verify_hashes(args.directory, args.hashfile, args.failedfile)
