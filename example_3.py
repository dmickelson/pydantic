import enum
import hashlib
import re
from typing import Any, Self
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
    SecretStr,
)

"""Key expansions and improvements in example_3.py:
1. Introduction of serialization methods: field_serializer and model_serializer decorators are used to customize how the User model is serialized.
2. Additional model validator: A post-validation check ensures that only users named "Arjan" can have the Admin role.
3. Enhanced Role enum: Includes a 'User' role with value 0.
4. Improved password handling: The password field is now excluded from serialization by default.
5. Demonstration of various serialization methods in the main function.

This example builds upon the previous ones by introducing advanced serialization techniques and demonstrating how to customize the output of your Pydantic models. 
It shows how to control what data is included in the serialized output and how it's formatted, which is crucial for API development and data transfer scenarios.

The main function in example_3.py demonstrates different ways to serialize the User object, showcasing the flexibility of Pydantic's serialization capabilities. 
This is particularly useful when you need to control how your data is presented in different contexts, such as API responses or database storage.
"""
# Regular expressions for input validation (same as example_2.py)
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")

# Enhanced Role enum using IntFlag (similar to example_2.py, but with an additional 'User' role)


class Role(enum.IntFlag):
    User = 0
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8

# Enhanced User model with additional validations and serialization methods


class User(BaseModel):
    name: str = Field(examples=["Example"])
    email: EmailStr = Field(
        examples=["user@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user", exclude=True
    )
    role: Role = Field(
        description="The role of the user",
        examples=[1, 2, 4, 8],
        default=0,
        validate_default=True,
    )

    # Field-level validators (similar to example_2.py)
    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and be at least 2 characters long"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {int: lambda x: Role(
            x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError):
            raise ValueError(
                f'Role is invalid, please use one of the following: {", ".join([x.name for x in Role])}'
            )

    # Model-level validators (expanded from example_2.py)
    @model_validator(mode="before")
    @classmethod
    def validate_user_pre(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "name" not in v or "password" not in v:
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password cannot contain name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number"
            )
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()
        return v

    @model_validator(mode="after")
    def validate_user_post(self, v: Any) -> Self:
        if self.role == Role.Admin and self.name != "Arjan":
            raise ValueError("Only Arjan can be an admin")
        return self

    # New serialization methods
    @field_serializer("role", when_used="json")
    @classmethod
    def serialize_role(cls, v) -> str:
        return v.name

    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info) -> dict[str, Any]:
        if not info.include and not info.exclude:
            return {"name": self.name, "role": self.role.name}
        return serializer(self)

# Main function demonstrating serialization


def main() -> None:
    data = {
        "name": "Arjan",
        "email": "example@arjancodes.com",
        "password": "Password123",
        "role": "Admin",
    }
    user = User.model_validate(data)
    if user:
        print(
            "The serializer that returns a dict:",
            user.model_dump(),
            sep="\n",
            end="\n\n",
        )
        print(
            "The serializer that returns a JSON string:",
            user.model_dump(mode="json"),
            sep="\n",
            end="\n\n",
        )
        print(
            "The serializer that returns a json string, excluding the role:",
            user.model_dump(exclude=["role"], mode="json"),
            sep="\n",
            end="\n\n",
        )
        print("The serializer that encodes all values to a dict:",
              dict(user), sep="\n")


if __name__ == "__main__":
    main()
