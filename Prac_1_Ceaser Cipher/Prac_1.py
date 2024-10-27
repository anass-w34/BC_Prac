
def caesar_cipher_ascii(text, shift, encrypt=True):
    result = ''
    shift = shift % 26  # Ensure the shift is within 0-25
    for char in text:
        if 'a' <= char <= 'z':
            base = 97  # ASCII value of 'a'
            offset = (ord(char) - base + (shift if encrypt else -shift)) % 26
            result += chr(base + offset)
        elif 'A' <= char <= 'Z':
            # For uppercase letters
            base = 65  # ASCII value of 'A'
            offset = (ord(char) - base + (shift if encrypt else -shift)) % 26
            result += chr(base + offset)
        else:
            result += char
    return result


def main():
    text = input("Enter the text to be processed: ")
    shift = int(input("Enter the shift value (integer): "))
    action = input("Enter 'encrypt' to encrypt, 'decrypt' to decrypt, or 'both': ").strip().lower()

    if action not in ['encrypt', 'decrypt', 'both']:
        print("Invalid action. Please enter 'encrypt', 'decrypt', or 'both'.")
        return

    encrypt = action == 'encrypt'
    decrypt = action == 'decrypt'
    both = action == 'both'

    if both:
        encrypted_text = caesar_cipher_ascii(text, shift, encrypt=True)
        decrypted_text = caesar_cipher_ascii(encrypted_text, shift, encrypt=False)
        print(f"Encrypted Text: {encrypted_text}\nDecrypted Text: {decrypted_text}")
    else:
        processed_text = caesar_cipher_ascii(text, shift, encrypt=encrypt)
        if encrypt:
            print(f"Encrypted Text: {processed_text}")
        elif decrypt:
            print(f"Decrypted Text: {processed_text}")


if __name__ == "__main__":
    main()


------------------------------- OUTPUT-----------------------------------------------
D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_1.py 
Enter the text to be processed: Hello
Enter the shift value (integer): 3
Enter 'encrypt' to encrypt, 'decrypt' to decrypt, or 'both': both
Encrypted Text: Khoor
Decrypted Text: Hello

Process finished with exit code 0


*******************************************************************************************

D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_1.py 
Enter the text to be processed: Hello
Enter the shift value (integer): 3
Enter 'encrypt' to encrypt, 'decrypt' to decrypt, or 'both': encrypt
Encrypted Text: Khoor

Process finished with exit code 0

**********************************************************************************************
D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_1.py 
Enter the text to be processed: hello
Enter the shift value (integer): 3
Enter 'encrypt' to encrypt, 'decrypt' to decrypt, or 'both': decrypt
Decrypted Text: ebiil

Process finished with exit code 0


