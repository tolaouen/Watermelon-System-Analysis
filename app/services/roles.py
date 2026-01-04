from typing import List, Optional

from app.models.roles import Role
from app.models.permissions import Permission

from extensions import db

class RoleService:
# Get all view role in the column
    @staticmethod
    def get_role_all() -> List[Role]:
        return Role.query.order_by(Role.id).all()
    
# Get single role view by id in the column
    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)
    
# Create role permission
    @staticmethod
    def create_role(data: dict, permission_id: Optional[int] = None) -> Role:
        role = Role(
            name = data["name"],
            description = data.get("description", "")
        )

        if permission_id:
            permission = db.session.scalars(
                db.select(Permission).filter(Permission.id.in_(permission_id))
            )
            role.permissions = list(permission)
        
        db.session.add(role)
        db.session.commit()
        return role
    
# Update role service permission

    @staticmethod
    def update_role(role: Role, data: dict, permission_id: Optional[int] = None) -> Role:
        role.name = data["name"]
        role.description = data.get("description", "")

        if permission_id:
            permission: List[Permission] = []
            if permission_id:
                permission = db.session.scalars(
                    db.select(Permission).filter(Permission.id.in_(permission_id))
                )
            role.permissions = list(permission)

        db.session.commit()
        return role

# Delete role service permission

    @staticmethod
    def delete_role(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()


