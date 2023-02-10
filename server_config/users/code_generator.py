import random
import string
import base64
import hashlib
random.seed(9123)
code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

print(code_verifier)
print("++++++")
print(code_challenge)


# http://127.0.0.1:8000/o/authorize/?response_type=code&
# code_challenge=f7pBXnqAX8vVNt7uYBlOWMWRVPzsnOjtV-R3UCW6njU&
# code_challenge_method=S256&
# client_id=tBgO5UYdYliUytYnl2fPzdM3uhYCeV02cSlgXjqB&
# redirect_uri=http://127.0.0.1:8000/noexist/callback

# curl -X POST -H "Cache-Control: no-cache"
# -H "Content-Type: application/x-www-form-urlencoded" 
# "http://127.0.0.1:8000/o/token/"
# -d "client_id=tBgO5UYdYliUytYnl2fPzdM3uhYCeV02cSlgXjqB"
# -d "client_secret=44YyYPvQe1enMvrvrQfusByrRybdr6kSv78bltfkqCeYfJHgG7xPKN49sDBXlGPb7KIO66T0mVTi7DsisnfkK22h9xbTHqwxgPBoY2FvXUC8OFeNiYoaxL4twyzXj0zz" 
# -d "code=6GscK6hCVKUQ1JXba3GYtYrPcYwDEi" -d "code_verifier=Q1dZWjRUQlBDNThVREE5QTM5OE5EOEszRFUxQkg4UVhERExBTzI0RFdBRkNWNjFPMTdRNUNZOTFCTUYwSERUVDJNV1BSQzZDWk5GTVY5RUVMWTBYSDdGTTlQRkMzUFQ5MFg4OEdJ" 
# -d "redirect_uri=http://127.0.0.1:8000/noexist/callback" 
# -d "grant_type=authorization_code"