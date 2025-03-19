import hashlib
import json

# Method for dictionaries and/or blocks for other uses. Call this inside a class.
def hash_block(block):
    translate_block = json.dumps(block, sort_keys=True)
    hashed_block = hashlib.sha256(translate_block.encode()).hexdigest()
    return hashed_block

# Default function of the hasher module.
def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        file_binary = file.read(4096)
        while file_binary:
            hasher.update(file_binary)
            file_binary = file.read(4096)
    return hasher.hexdigest()
    print(hash_file)


if __name__ == "__main__":
    filepath = input("Enter the path of the file you want to hash: ")
    print(hash_file(filepath))