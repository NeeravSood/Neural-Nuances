import hashlib

def calculate_checksum(file_path, algorithm='sha256'):
    """Calculate the checksum of a file using the specified algorithm."""
    hash_algo = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def verify_file_integrity(file_path, expected_checksum, algorithm='sha256'):
    """Verify that the file's checksum matches the expected checksum."""
    actual_checksum = calculate_checksum(file_path, algorithm)
    return actual_checksum == expected_checksum
