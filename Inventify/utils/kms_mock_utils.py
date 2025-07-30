# Inventify/utils/kms_mock_utils.py
import base64
import logging

logger = logging.getLogger(__name__)

def encrypt_with_kms(plaintext_data) -> bytes:
    """
    Mocks KMS encryption for local testing.
    Accepts both str and bytes. If a string is provided, it's first
    encoded to UTF-8 bytes. Then, it base64 encodes the result.
    """
    data_to_encrypt = None
    print("40")

    if isinstance(plaintext_data, str):
        data_to_encrypt = plaintext_data.encode('utf-8')
        logger.debug(f"MOCK KMS: Encrypting string (length {len(plaintext_data)}).")
    elif isinstance(plaintext_data, bytes):
        data_to_encrypt = plaintext_data
        logger.debug(f"MOCK KMS: Encrypting bytes (length {len(plaintext_data)}).")
    else:
        raise TypeError("Input to encrypt_with_kms must be a string or bytes.")
    
    return base64.b64encode(data_to_encrypt)

def decrypt_with_kms(ciphertext: bytes) -> bytes:
    """
    Mocks KMS decryption for local testing.
    In a real scenario, this would interact with Azure Key Vault.
    Here, it simply base64 decodes the ciphertext.
    """
    logger.debug(f"MOCK KMS: Decrypting (base64 decoding) '{ciphertext}' for local testing.")
    try:
        # Attempt to base64 decode. If it fails, it means it wasn't mock-encrypted.
        return base64.b64decode(ciphertext)
    except Exception as e:
        logger.error(f"MOCK KMS Decryption error: {e}. Returning original ciphertext (maybe plaintext or not mock-encrypted).", exc_info=True)
        return ciphertext # Fallback if ciphertext isn't valid base64