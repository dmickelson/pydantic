from pydantic import create_model, BaseModel, Field

"""
This example demonstrates dynamic model creation in Pydantic.
It shows how to create models at runtime based on certain conditions,
allowing for flexible and adaptable data structures.

This example demonstrates the capability of dynamic model creation in Pydantic. Key points:
1. It uses the create_model function from Pydantic to generate models at runtime.
2. The create_user_model function dynamically creates different user models based on whether the user is an admin or not.
4. For admin users, an additional access_level field is added to the model.
4. The example shows how to create instances of these dynamically created models and how they behave differently based on their structure.

This capability is particularly useful when you need to create models that vary based on runtime conditions, 
allowing for more flexible and adaptable data structures in your application.
"""


def create_user_model(admin: bool = False):
    # Define base fields for all user models
    fields = {
        "username": (str, ...),  # ... means the field is required
        "email": (str, ...),
    }

    # Add an additional field for admin users
    if admin:
        # ge=5 means greater than or equal to 5
        fields["access_level"] = (int, Field(ge=5))

    # Create and return the dynamic model
    return create_model("User", **fields)


def main():
    # Create two different user models
    RegularUser = create_user_model()
    AdminUser = create_user_model(admin=True)

    # Create instances of these models
    regular_user = RegularUser(username="john", email="john@example.com")
    admin_user = AdminUser(
        username="admin", email="admin@example.com", access_level=10)

    # Print the created users
    print(f"Regular user: {regular_user}")
    print(f"Admin user: {admin_user}")


if __name__ == "__main__":
    main()
