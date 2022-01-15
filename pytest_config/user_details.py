import base64

user_details = {
        "user_1": {
            "username": "user_1",
            "password": "cGFzc18x"
        },
        "user_2": {
            "username": "user_2",
            "password": "cGFzc18y"
        },
        "user_3": {
            "username": "user_3",
            "password": "cGFzc18z"
        },
        "user_4": {
            "username": "user_4",
            "password": "cGFzc180"
        },
        "user_5": {
            "username": "user_5",
            "password": "cGFzc181"
        },
        "invalid_user_1": {
            "username": "abc_1",
            "password": "cHFyXzE="
        },
        "invalid_user_2": {
            "username": "xyz_2",
            "password": "c3R1XzI="
        },
        "mismatch_user_1": {
            "username": "user_1",
            "password": "cGFzc18y"
        }
}


def encode_string(text, format='ascii'):
    format_encode = text.encode(format)
    encoded = base64.b64encode(format_encode).decode(format)
    return encoded


def decode_string(encoded_text, format='ascii'):
    decoded = base64.b64decode(encoded_text).decode(format)
    return decoded
