import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import json



SECRET_KEY = b'ThisIsASecretKey'  # Change this to your secret key



# def encode_dict(secret_key, data):
#     print(data)
#     # Convert dictionary to JSON string
#     json_data = json.dumps(data, ensure_ascii=False)
#     print(json_data)
    
#     # Generate a random initialization vector
#     iv = get_random_bytes(AES.block_size)
    
#     # Create AES cipher object
#     cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
#     # Pad the JSON data
#     padded_data = pad(json_data.encode(), AES.block_size)
    
#     # Encrypt the data
#     encrypted_data = cipher.encrypt(padded_data)
    
#     print(iv + encrypted_data)
    
#     # Return the IV and encrypted data as bytes
#     return iv + encrypted_data

# def decode_dict(secret_key, encoded_data):
#     # Extract IV from the encoded data
#     iv = encoded_data[:AES.block_size]
    
#     # Create AES cipher object
#     cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
#     # Decrypt the data
#     decrypted_data = cipher.decrypt(encoded_data[AES.block_size:])
    
#     # Unpad the decrypted data
#     unpadded_data = unpad(decrypted_data, AES.block_size)
    
#     # Decode JSON data
#     decoded_data = json.loads(unpadded_data.decode())
    
#     return decoded_data









def encode_dict(secret_key, data):
    # Convert dictionary to JSON string
    json_data = json.dumps(data)
    
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher object
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
    # Pad the JSON data
    padded_data = pad(json_data.encode(), AES.block_size)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Combine IV and encrypted data and encode as base64 string
    encoded_data = base64.b64encode(iv + encrypted_data).decode('utf-8')
    
    return encoded_data

def decode_dict(secret_key, encoded_data):
    # Decode base64 string
    encoded_data = base64.b64decode(encoded_data)
    
    # Extract IV from the encoded data
    iv = encoded_data[:AES.block_size]
    
    # Create AES cipher object
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
    # Decrypt the data
    decrypted_data = cipher.decrypt(encoded_data[AES.block_size:])
    
    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)
    
    # Decode JSON data
    decoded_data = json.loads(unpadded_data.decode())
    
    return decoded_data