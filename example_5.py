from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

"""
This example demonstrates:
1. Advanced config management using ConfigDict
2. Alias generation for field names
3. Frozen models (immutability after creation)
4. Strict extra fields handling
"""

"""
This example demonstrates several advanced Pydantic features:
1. ConfigDict usage for detailed model configuration
2. Custom alias generation for field names
3. Frozen models to enforce immutability
4. Strict handling of extra fields
5. Validation on assignment after model creation

The difference between configuration (as shown in example_5.py) and application settings (as shown in example_7_settings_management.py) is:
Configuration (example_5.py):
- Focuses on how a specific Pydantic model behaves
- Defines rules for data validation, serialization, and model behavior
- Is typically set at the class level and affects instances of that class

Application Settings (example_7_settings_management.py):
- Deals with application-wide configuration values
- Manages external configuration sources like environment variables or .env files
- Is typically used to store and retrieve application-specific settings that might change between environments

In essence, configuration in example_5.py is about model behavior, while application settings in example_7_settings_management.py is about managing 
application-wide configuration values.

"""


class UserConfig(BaseModel):
    model_config = ConfigDict(
        # Allows populating model by field name and alias
        allow_population_by_field_name=True,
        validate_assignment=True,  # Validates values on assignment after model creation
        extra='forbid',  # Forbids extra fields not defined in the model
        alias_generator=lambda x: x.upper(),  # Generates aliases for all fields
    )

    username: str = Field(alias='user')
    email: str
    age: Optional[int] = None
    tags: List[str] = []

    def __init__(self, **data):
        super().__init__(**data)
        # Makes the model immutable after creation
        self.model_config['frozen'] = True


def main():
    # Creating a user with aliases
    user = UserConfig(user='john_doe', EMAIL='john@example.com', AGE=30)
    print(f"User created: {user.model_dump()}")

    # Accessing fields using aliases
    print(f"Username (using alias): {user.USER}")

    # Attempting to add an extra field (will raise an error)
    try:
        user_dict = user.model_dump()
        user_dict['extra_field'] = 'This will fail'
        UserConfig(**user_dict)
    except ValueError as e:
        print(f"Error when adding extra field: {e}")

    # Attempting to modify a frozen model (will raise an error)
    try:
        user.age = 31
    except ValueError as e:
        print(f"Error when modifying frozen model: {e}")


if __name__ == "__main__":
    main()
