from dataclasses import dataclass
from flask_security import RoleMixin
from controllers.db import db

roles_users_table = db.Table(
    "role_user",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

@dataclass
class Role(db.Model, RoleMixin):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __init__(self, name, description):
        self.name = name
        self.description = description