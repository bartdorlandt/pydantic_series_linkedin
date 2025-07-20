from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


class UserList(BaseModel):
    users: list[User]


user_json = {
    "users": [
        {"id": 1, "name": "John Doe", "email": "some@email.com"},
        {"id": 2, "name": "Jane Foo", "email": "jane@foo.com"},
    ]
}

user = UserList(**user_json)

print(user.users[0].name)
print(user)
