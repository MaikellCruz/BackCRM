from app.security import get_password_hash, verify_password

p = 'x' * 200
h = get_password_hash(p)
print('hash preview:', h[:80])
print('verify long:', verify_password(p, h))
print('verify truncated:', verify_password(p[:72], h))
