# Pydantic Examples

This repository contains examples demonstrating key features of Pydantic. Each example file focuses on specific aspects of Pydantic's functionality.

## Example Files and Key Features

1. example.py

   - Basic Pydantic model creation
   - Field types and validation
   - Use of Pydantic's Field for additional metadata

2. example_2.py

   - Advanced field validation with regex
   - Custom validators using @field_validator
   - Model-level validation using @model_validator
   - Password hashing example

3. example_3.py

   - Custom serialization methods
   - Field serializers with @field_serializer
   - Model serializers with @model_serializer
   - Advanced role-based validation

4. example_4.py

   - Integration with FastAPI
   - UUID usage for unique identifiers
   - In-memory storage of model instances
   - API endpoint creation and routing

5. example_5.py

   - Advanced configuration using ConfigDict
   - Alias generation for field names
   - Frozen models (immutability after creation)
   - Strict extra fields handling

6. example_6_dynamic_models.py

   - Dynamic model creation at runtime
   - Conditional field addition based on parameters

7. example_7_settings_management.py
   - Application settings management
   - Environment variable loading
   - Secure handling of sensitive data

These examples cover a wide range of Pydantic's features, from basic model creation to advanced configuration and integration with web frameworks.

## Dependencies

The examples in this repository depend on the following Python modules:

- pydantic
- fastapi
- pydantic_settings
- enum
- typing
- datetime
- uuid
- hashlib
- re

Make sure to install these dependencies before running the examples.
