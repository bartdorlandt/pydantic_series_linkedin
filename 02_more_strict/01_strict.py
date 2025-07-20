from pydantic import BaseModel, EmailStr, Field, PositiveInt


class User(BaseModel):
    id: PositiveInt
    name: str = Field(min_length=1)
    email: EmailStr


user_json = {"id": 1, "name": "John Doe", "email": "some@email.com"}

user = User(**user_json)

print(user)
print(user.name)
print(user.email)

print(user.model_dump_json(indent=2))
