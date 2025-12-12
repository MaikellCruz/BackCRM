"""Seed script para criar um role 'admin' e um usuário admin.

Uso:
    python scripts/seed_admin.py

Observação: usa a senha 'admin' (plain) e armazena o hash no banco.
"""

from roles.role_model import Role
from users.user_model import User
from security import get_password_hash
from passlib.exc import MissingBackendError
import sys

from database import SessionLocal


def seed_admin(email: str = "admin@example.com", password: str = "admin"):
    db = SessionLocal()
    try:
        # Verifica se o role admin já existe
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print(f"Role 'admin' criado com id={admin_role.id}")
        else:
            print(f"Role 'admin' já existe id={admin_role.id}")

        # Verifica se usuário admin já existe pelo email
        admin_user = db.query(User).filter(User.email == email).first()
        if not admin_user:
            try:
                hashed = get_password_hash(password)
            except MissingBackendError:
                print("Erro: backend de hash (bcrypt) não está disponível. Instale 'bcrypt' via pip: python -m pip install bcrypt")
                sys.exit(1)

            admin_user = User(
                email=email,
                hashed_password=hashed,
                full_name="Admin",
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Usuário admin criado: email={email} id={admin_user.id}")
        else:
            print(f"Usuário admin já existe: email={email} id={admin_user.id}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
