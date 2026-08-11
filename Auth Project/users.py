from fastapi import APIRouter, Depends

from models import User
from security import get_current_user, require_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/admin")
def admin_dashboard(current_user:User=Depends(require_admin)):
    return{
    "message":"Welcome admin",
    "username":current_user.username,
    "role":current_user.role}
