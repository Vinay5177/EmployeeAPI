import hmac
import hashlib
import base64

USERNAME = "admin@example.com"
CLIENT_ID = "4c4akm94rlgqbirnlkek220kn8"
CLIENT_SECRET = "1iemula931bv8fdgv3pi3qmtpqndp6plc5n8oqirb1p25kuktddm"

message = USERNAME + CLIENT_ID

secret_hash = base64.b64encode(
    hmac.new(
        CLIENT_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
).decode()

print("SECRET_HASH:")
print(secret_hash)