from typing import List, Optional

from app.models.users import User
from app.models.roles import Role

from extensions import db

class UserService:

# Get all view user in colum
    @staticmethod
    def get_user_all() -> List[User]:
        return User.query.order_by(User.id.asc()).all()
    
# Get single view user in column by id
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
# Create user Account
    @staticmethod
    def create_user(data: dict, password: str, role_id: Optional[int] = None) -> User:
        user = User(
            username = data["username"],
            email = data["email"],
            full_name = data["full_name"],
            is_active = data.get("is_active", True)
        )

        user.set_password(password)

        if role_id:
            role = db.session.get(Role, role_id)
            if role:
                user.roles = [role]
        

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user
    
# Update user data in column
    @staticmethod
    def update_user(user: User, data: dict, password: Optional[str] = None, role_id: Optional[int] = None) -> User:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True)

        if password:
            user.set_password(password)
        
        if role_id:
            role = db.session.get(Role, role_id)
            if role:
                user.roles = [role]

        db.session.commit()
        return user

# Delete view user in column
    @staticmethod
    def delete_user(user: User) -> None:
        db.session.delete(user)
        db.session.commit()