import hashlib
from base64 import b64decode
from Crypto.Cipher import AES

def derive_aes_key(password: str | bytes, salt: str) -> bytes:
    """
    Derives a 256-bit AES key using PBKDF2.
    Handles both str and bytes for password.
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.pbkdf2_hmac(
        'sha256',
        password,
        salt.encode('utf-8'),
        100000,
        dklen=32
    )


def decrypt_field_if_needed(encrypted_text_base64: str, aes_key_bytes: bytes) -> str:
    """
    Attempts to decrypt a field. If it's not encrypted or decryption fails, returns the original value.
    """
    try:
        # Only attempt decryption if it's a base64 string of reasonable length
        
        if not isinstance(encrypted_text_base64, str) or len(encrypted_text_base64) < 24:
            return encrypted_text_base64  # likely not encrypted
        
        encrypted_data = b64decode(encrypted_text_base64)
        iv = encrypted_data[:12]
        ciphertext_and_tag = encrypted_data[12:]

        cipher = AES.new(aes_key_bytes, AES.MODE_GCM, nonce=iv)
        decrypted_bytes = cipher.decrypt_and_verify(
            ciphertext_and_tag[:-16],  # ciphertext
            ciphertext_and_tag[-16:]   # tag
        )
        print("4")
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"❌ Decryption failed (field may be plaintext): {e}")
        return encrypted_text_base64  # fallback: return original value