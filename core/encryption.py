# 加密模块
# 提供加密/解密接口
from cryptography.fernet import Fernet
import base64
import os

KEY_PATH = os.path.join(os.path.dirname(__file__), '../config/key.bin')

def generate_key():
    key = Fernet.generate_key()
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
    with open(KEY_PATH, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, 'rb') as f:
        return f.read()

def encrypt_data(data: str) -> str:
    key = load_key()
    f = Fernet(key)
    token = f.encrypt(data.encode())
    return base64.b64encode(token).decode('utf-8')

def decrypt_data(token_b64: str) -> str:
    key = load_key()
    f = Fernet(key)
    token = base64.b64decode(token_b64)
    return f.decrypt(token).decode()
