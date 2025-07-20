from pydantic import BaseModel, EmailStr, Field, PositiveInt


class User(BaseModel):
    id: PositiveInt
    name: str = Field(min_length=1)
    email: EmailStr


user_json = {"id": -1, "name": "John Doe", "email": "some@email.com"}

user = User(**user_json)

# Traceback (most recent call last):
#   File "/Users/bart/git/pydantic_series/02_more_strict/wrong_id.py", line 12, in <module>
#     user = User(**user_json)
#   File "/Users/bart/git/pydantic_series/.venv/lib/python3.13/site-packages/pydantic/main.py", line 253, in __init__
#     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
# pydantic_core._pydantic_core.ValidationError: 1 validation error for User
# id
#   Input should be greater than 0 [type=greater_than, input_value=-1, input_type=int]
#     For further information visit https://errors.pydantic.dev/2.11/v/greater_than

print(user)
print(user.name)
print(user.email)

print(user.model_dump_json(indent=2))
