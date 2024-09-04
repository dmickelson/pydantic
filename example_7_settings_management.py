from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

"""
This code demonstrates several important concepts in Pydantic settings management:
1. Use of BaseSettings: The AppSettings class inherits from BaseSettings, which is specifically designed for handling application configuration.
2. Environment Variable Loading: By using BaseSettings, the code can automatically load configuration values from environment variables or a .env file.
3. Configuration of Settings Behavior: The SettingsConfigDict is used to specify the .env file and its encoding, allowing for flexible configuration sources.
4. Type Safety: Each configuration field is annotated with its expected type (str, SecretStr), ensuring type safety and validation.
5. Default Values: Some fields (like app_name) have default values, while others (admin_email, secret_key) are required to be set in the environment or .env file.
6. Secure Handling of Sensitive Data: The use of SecretStr for secret_key demonstrates how to handle sensitive information securely.
7. Easy Access to Settings: The main function shows how easily the settings can be accessed once the AppSettings instance is created.

This example showcases Pydantic's powerful features for managing application settings, combining ease of use with type safety and secure handling of sensitive data. 
It's particularly useful for applications that need to manage configuration across different environments (development, testing, production) 
while maintaining security and type safety.
"""
# AppSettings class inherits from BaseSettings, which is designed for handling configuration


class AppSettings(BaseSettings):
    # Configuration for the settings, specifying the .env file and its encoding
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    # Define configuration fields with their types and default values
    app_name: str = "MyApp"
    admin_email: str
    secret_key: SecretStr  # SecretStr is used for sensitive data


def main():
    # Create an instance of AppSettings, which will automatically load values from environment variables or .env file
    settings = AppSettings()

    # Print the configuration values
    print(f"App Name: {settings.app_name}")
    print(f"Admin Email: {settings.admin_email}")
    print(f"Secret Key: {settings.secret_key.get_secret_value()}")


if __name__ == "__main__":
    main()
