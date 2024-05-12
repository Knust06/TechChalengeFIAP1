from cryptography.fernet import Fernet

def criptogradar(key, text):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text

def descriptogradar(key, encrypted_text):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text

chave_fernet =b'yyG38ujD52zYjrMAJwomcyCjEJm5Fzg-4zTJdl3GX2U='
print(chave_fernet)
print(chave_fernet.decode())
