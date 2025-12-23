try:
    print("Testing bcrypt import...")
    import bcrypt
    print(f"Bcrypt version: {bcrypt.__version__}")
except ImportError as e:
    print(f"Bcrypt Import Failed: {e}")

try:
    print("Testing passlib context...")
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash_val = pwd_context.hash("test_password")
    print(f"Hashing Success: {hash_val[:10]}...")
except Exception as e:
    print(f"Hashing Failed: {e}")
