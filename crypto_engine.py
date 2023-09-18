from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def string_to_byte_array(string):
    encoded_bytes = string.encode('utf-8')
    byte_array = base64.b64decode(encoded_bytes)
    return byte_array

def encrypt_message(key, plaintext):
    # Create an AES cipher object with the key and AES.MODE_ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Pad the plaintext to be a multiple of 16 bytes (AES block size)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # Convert the ciphertext to a string
    ciphertext_str = ciphertext.hex()

    # Print the ciphertext
    return ciphertext_str


def decrypt_message(key, ciphertext_str):
    # Create a new AES cipher object with the key and AES.MODE_ECB mode
    decrypt_cipher = AES.new(key, AES.MODE_ECB)

    # Convert the ciphertext string back to bytes
    ciphertext_bytes = bytes.fromhex(ciphertext_str)

    # Decrypt the ciphertext
    decrypted_plaintext = decrypt_cipher.decrypt(ciphertext_bytes)

    # Remove padding from the decrypted plaintext
    unpadded_plaintext = unpad(decrypted_plaintext, AES.block_size)

    # Convert the unpadded plaintext to a string
    plaintext = unpadded_plaintext.decode()

    # Print the decrypted plaintext
    return plaintext