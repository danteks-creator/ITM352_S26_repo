from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

encodeed_text = cipher_suite.encrypt(b"This is a really secret message")
print(f"Encoded text: {encodeed_text}")

#use the cryptography library to encode and decode a message
decoded_text = cipher_suite.decrypt(encodeed_text)
print(f"Decoded text: {decoded_text.decode('utf-8')}")