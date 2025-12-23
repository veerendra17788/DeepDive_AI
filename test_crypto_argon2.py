try:
    print("Testing argon2-cffi import...")
    import argon2
    print(f"Argon2 version: {argon2.__version__}")
except ImportError as e:
    print(f"Argon2 Import Failed: {e}")

try:
    print("Testing passlib context with argon2...")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    hash_val = pwd_context.hash("test_password_long_enough_to_be_interesting")
    print(f"Hashing Success: {hash_val[:10]}...")
    
    # Verify
    verify = pwd_context.verify("test_password_long_enough_to_be_interesting", hash_val)
    print(f"Verification Success: {verify}")
except Exception as e:
    print(f"Hashing Failed: {e}")
