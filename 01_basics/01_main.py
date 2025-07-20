from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


user_json = {"id": 1, "name": "John Doe", "email": "some@email.com"}

user = User(**user_json)

print(user)
print(user.name)
