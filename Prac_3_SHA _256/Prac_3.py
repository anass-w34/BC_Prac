import hashlib

def sha256_hash(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    hash_value = sha256.hexdigest()
    block_size = sha256.block_size
    digest_size = sha256.digest_size
    return hash_value, block_size, digest_size

if __name__ == "__main__":
    user_input = input("Enter the string to hash: ")
    hash_output, block_size, digest_size = sha256_hash(user_input)
    print(f"SHA-256 Hash: {hash_output}")
    print(f"Block Size: {block_size} bytes")
    print(f"Digest Size: {digest_size} bytes")


------------------------- OUTPUT -------------------------------------------------

D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_3.py 
Enter the string to hash: hello
SHA-256 Hash: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
Block Size: 64 bytes
Digest Size: 32 bytes

Process finished with exit code 0

