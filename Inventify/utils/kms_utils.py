import os
import logging
# from django.conf import settings
from Inventify.settings import AZURE_KEY_VAULT_URL, AZURE_KEY_VAULT_KEY_NAME

# --- AZURE KEY VAULT IMPORTS ---
# Install these: pip install azure-identity azure-keyvault-keys
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient
from azure.core.exceptions import HttpResponseError # For handling Key Vault specific errors

logger = logging.getLogger(__name__)

# --- AZURE KEY VAULT CLIENT INITIALIZATION ---
# It's good practice to initialize the KMS client once globally or ensure it's efficiently
# managed to avoid re-initializing on every encryption/decryption call.
_azure_kms_crypto_client = None

def _get_azure_kms_client():
    """
    Initializes and returns an Azure Key Vault CryptographyClient.
    This client is used for performing cryptographic operations (encrypt/decrypt)
    with the key in Azure Key Vault.
    """
    global _azure_kms_crypto_client
    if _azure_kms_crypto_client is None:
        try:
            key_vault_url = AZURE_KEY_VAULT_URL
            key_name = AZURE_KEY_VAULT_KEY_NAME

            if not key_vault_url or not key_name:
                raise ValueError("AZURE_KEY_VAULT_URL and AZURE_KEY_VAULT_KEY_NAME must be configured in Django settings.")

            # DefaultAzureCredential will try various authentication methods:
            # environment variables, managed identity, Azure CLI, etc.
            # On Azure App Service with Managed Identity enabled, it will automatically use that.
            # For production, it's often recommended to be more explicit (e.g., ManagedIdentityCredential)
            # but DefaultAzureCredential is fine for development and often works in production too.
            credential = DefaultAzureCredential()

            # KeyClient is used to manage keys (get key properties, versions)
            key_client = KeyClient(vault_url=key_vault_url, credential=credential)
            
            # Retrieve the key to get its full ID for the CryptographyClient
            key = key_client.get_key(key_name)
            
            _azure_kms_crypto_client = CryptographyClient(key=key, credential=credential)
            logger.info("Azure Key Vault CryptographyClient initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize Azure Key Vault client: {e}", exc_info=True)
            raise RuntimeError("KMS client initialization failed. Please check your Azure Key Vault URL, key name, and managed identity permissions.") from e
    return _azure_kms_crypto_client


# --- ENCRYPTION FUNCTION ---
def encrypt_with_kms(plaintext_data: bytes) -> bytes:
    """
    Encrypts plaintext data using an RSA key in Azure Key Vault (RSA-OAEP algorithm).

    Args:
        plaintext_data (bytes): The data to be encrypted. Max size for direct RSA-OAEP
                                encryption is key_size_in_bytes - 42 bytes (e.g., 256-42 for 2048-bit key).
                                For larger data, implement envelope encryption.

    Returns:
        bytes: The ciphertext (encrypted data).

    Raises:
        RuntimeError: If encryption fails.
        TypeError: If input data is not bytes.
    """
    print("26")
    if not isinstance(plaintext_data, bytes):
        raise TypeError("Input data for encryption must be bytes.")
    
    # IMPORTANT NOTE ON RSA ENCRYPTION LIMITS:
    # Direct RSA encryption (like RSA_OAEP) has a strict size limitation.
    # For a 2048-bit RSA key, you can encrypt about 214 bytes (256 - 42 bytes of OAEP overhead).
    # For a 3072-bit RSA key, you can encrypt about 342 bytes (384 - 42 bytes).
    # For a 4096-bit RSA key, you can encrypt about 470 bytes (512 - 42 bytes).
    # This means you CANNOT directly encrypt large images with RSA-OAEP.
    # You MUST implement "Envelope Encryption" for images:
    # 1. Generate a random, symmetric Data Encryption Key (DEK) locally (e.g., AES-256 key).
    # 2. Encrypt your actual image data with this DEK (using a fast symmetric algorithm like AES-256-CBC/GCM).
    # 3. Encrypt the DEK (which is small) using your RSA key in Azure Key Vault (using RSA_OAEP).
    # 4. Store both the encrypted DEK and the AES-encrypted image data.
    # 5. For decryption, retrieve the encrypted DEK, decrypt it with AKV, then use the decrypted DEK to decrypt the image.

    try:
        client = _get_azure_kms_client()
        # Ensure your plaintext_data is within the RSA encryption limits if directly encrypting.
        # If not, you need to implement Envelope Encryption as described above.
        encryption_result = client.encrypt("RSA_OAEP", plaintext_data)
        ciphertext = encryption_result.ciphertext
        logger.debug(f"Data encrypted using Azure Key Vault.")
        return ciphertext
    except HttpResponseError as e:
        logger.error(f"Azure Key Vault encryption error (HTTP status: {e.status_code}, code: {e.code}): {e.message}", exc_info=True)
        raise RuntimeError(f"KMS encryption failed: {e.message}") from e
    except Exception as e:
        logger.error(f"Unexpected error during Azure Key Vault encryption: {e}", exc_info=True)
        raise RuntimeError(f"KMS encryption failed: {e}") from e


# --- DECRYPTION FUNCTION ---
def decrypt_with_kms(ciphertext_data: bytes) -> bytes:
    """
    Decrypts ciphertext data using an RSA key in Azure Key Vault (RSA-OAEP algorithm).

    Args:
        ciphertext_data (bytes): The encrypted data to be decrypted. Must be bytes.

    Returns:
        bytes: The plaintext data.

    Raises:
        RuntimeError: If decryption fails.
        TypeError: If input data is not bytes.
    """
    if not isinstance(ciphertext_data, bytes):
        raise TypeError("Input data for decryption must be bytes.")

    try:
        client = _get_azure_kms_client()
        decryption_result = client.decrypt("RSA_OAEP", ciphertext_data)
        plaintext = decryption_result.plaintext
        logger.debug(f"Data decrypted using Azure Key Vault.")
        return plaintext
    except HttpResponseError as e:
        logger.error(f"Azure Key Vault decryption error (HTTP status: {e.status_code}, code: {e.code}): {e.message}", exc_info=True)
        raise RuntimeError(f"KMS decryption failed: {e.message}") from e
    except Exception as e:
        logger.error(f"Unexpected error during Azure Key Vault decryption: {e}", exc_info=True)
        raise RuntimeError(f"KMS decryption failed: {e}") from e