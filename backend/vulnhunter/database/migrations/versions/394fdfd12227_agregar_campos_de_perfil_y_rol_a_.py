"""Agregar campos de perfil y rol a usuarios

Revision ID: 394fdfd12227
Revises: 20260928_0002
Create Date: 2026-11-04 13:24:36.408349
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores de la migración (no tocar).
revision: str = '394fdfd12227'
down_revision: Union[str, None] = '20260928_0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregamos los campos de perfil a la tabla users.
    # nombre y apellido son obligatorios; el resto es opcional.
    op.add_column('users', sa.Column('nombre', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('apellido', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('rut', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('telefono', sa.String(length=30), nullable=True))
    op.add_column('users', sa.Column('fecha_nacimiento', sa.String(length=20), nullable=True))
    # role define el tipo de cuenta: "user" (cliente) o "admin". Por defecto "user".
    op.add_column('users', sa.Column('role', sa.String(length=20), server_default='user', nullable=False))
    # El RUT no se puede repetir entre usuarios.
    op.create_unique_constraint('uq_users_rut', 'users', ['rut'])


def downgrade() -> None:
    # Deshace lo anterior: quita el RUT único y borra las columnas agregadas.
    op.drop_constraint('uq_users_rut', 'users', type_='unique')
    op.drop_column('users', 'role')
    op.drop_column('users', 'fecha_nacimiento')
    op.drop_column('users', 'telefono')
    op.drop_column('users', 'rut')
    op.drop_column('users', 'apellido')
    op.drop_column('users', 'nombre')
