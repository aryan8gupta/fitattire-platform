from Inventify.utils.kms_utils import encrypt_with_kms, decrypt_with_kms
import logging

# Configure logging for better visibility during testing
# You can change level=logging.INFO to logging.DEBUG for more verbose output
logging.basicConfig(level=logging.INFO) 

# Test data - keep it small, as direct RSA encryption has size limits!
# For a 2048-bit RSA key, this plaintext should ideally be <= ~214 bytes.
# For a 3072-bit RSA key, this plaintext should ideally be <= ~342 bytes.
test_data = b"This is a small test string for Key Vault encryption."

print(f"\n--- KMS Integration Test ---")
print(f"Original Data: '{test_data.decode('utf-8')}' (Length: {len(test_data)} bytes)")

try:
    # Encrypt the data
    encrypted_data = encrypt_with_kms(test_data)
    print(f"Encrypted Data (bytes length): {len(encrypted_data)}")
    # Note: The raw encrypted bytes will not be human-readable.

    # Decrypt the data
    decrypted_data = decrypt_with_kms(encrypted_data)
    print(f"Decrypted Data: '{decrypted_data.decode('utf-8')}'")

    if test_data == decrypted_data:
        print("\nKMS Integration Test: SUCCESS! Data encrypted and decrypted correctly.")
    else:
        print("\nKMS Integration Test: FAILED! Decrypted data does not match original.")

except Exception as e:
    print(f"\nKMS Integration Test: FAILED! An error occurred during encryption/decryption:")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() # This will print the full traceback for debugging

print(f"--------------------------\n")