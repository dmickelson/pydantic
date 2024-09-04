from enum import auto, IntFlag
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
)

"""
Key features highlighted in the example:
- Use of IntFlag for creating a bitmask-style enumeration for user roles.
- Pydantic BaseModel for data validation and serialization.
- Use of Pydantic's Field for additional field metadata and validation.
- Special field types like EmailStr for email validation and SecretStr for password handling.
- The frozen=True attribute to make the email field immutable.
- Error handling with ValidationError to provide detailed feedback on validation failures.
- The model_validate method for creating and validating User instances.
- Separation of concerns with distinct functions for validation and main program flow.
"""

# IntFlag is used to create a bitmask-style enumeration
"""
Here's what's happening:

Each role (Author, Editor, Developer) is assigned a unique power-of-two integer value automatically by using auto(). For example, Author might be 1, Editor 2, Developer 4.

These values can be combined using bitwise operations. The | operator here performs a bitwise OR.

The Admin role is defined as a combination of all other roles using the | operator. This means an Admin has all the permissions of an Author, Editor, and Developer combined.

This setup allows for flexible role management:

You can easily check if a role includes certain permissions using bitwise operations.
You can combine roles to create custom permission sets.
It's memory-efficient as multiple roles can be represented in a single integer.
This bitmask-style enumeration is particularly useful in scenarios where you need to represent multiple flags or permissions in a single value, which is common in user role management systems.
"""


class Role(IntFlag):
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer  # Composite role

# Pydantic model for user data validation


class User(BaseModel):
    name: str = Field(examples=["Arjan"])
    email: EmailStr = Field(
        examples=["example@arjancodes.com"],
        description="The email address of the user",
        frozen=True,  # Email cannot be changed after initialization
    )
    password: SecretStr = Field(
        examples=["Password123"],
        description="The password of the user"
    )  # SecretStr hides the password in string representations
    role: Role = Field(default=None, description="The role of the user")

# Function to validate user data


def validate(data: dict[str, Any]) -> None:
    try:
        # Attempt to create a User instance with the provided data
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print("User is invalid")
        # Print detailed error messages for each validation failure
        for error in e.errors():
            print(error)


def main() -> None:
    # Example of valid user data
    good_data = {
        "name": "Arjan",
        "email": "example@arjancodes.com",
        "password": "Password123",
    }
    # Example of invalid user data
    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    # Validate both good and bad data
    validate(good_data)
    validate(bad_data)


if __name__ == "__main__":
    main()
