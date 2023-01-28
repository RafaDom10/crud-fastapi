from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("51850d89-e883-4d19-b264-5bba82300a28"),
        first_name="Xuxa",
        last_name="da Silva",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("fe8bd898-64c3-4685-9c4d-15dd5cc95856"),
        first_name="Daniel",
        last_name="Paladino",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.get("/api/v1/users/{user_id}")
async def fetch_user_by_id(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
