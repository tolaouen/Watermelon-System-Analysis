from extensions import db
from datetime import datetime
from app.models.associations import role_permissions
from app.models.associations import user_roles

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False, default=None)
    name = db.Column(db.String(120), unique=True, nullable=False, default=None)
    module = db.Column(db.String(90), default="General", nullable=False)
    description = db.Column(db.String(250), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship Table

    roles = db.relationship("Role", secondary=role_permissions, back_pupolates="permissions")
    
    def __repr__(self) -> str:
        return f"<Permissions {self.code}>"