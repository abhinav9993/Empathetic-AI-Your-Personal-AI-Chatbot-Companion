import base64

def encode_id(id):
    # Convert the integer ID to a byte string
    id_bytes = str(id).encode('utf-8')
    # Encode the ID using base64
    encoded_id_bytes = base64.urlsafe_b64encode(id_bytes)
    # Convert bytes back to a string
    encoded_id = encoded_id_bytes.decode('utf-8')
    return encoded_id

def decode_id(encoded_id):
    # Convert the encoded ID back into bytes
    encoded_id_bytes = encoded_id.encode('utf-8')
    # Decode the base64 string
    id_bytes = base64.urlsafe_b64decode(encoded_id_bytes)
    # Convert from bytes to string and then to an int
    id = int(id_bytes.decode('utf-8'))
    return id
