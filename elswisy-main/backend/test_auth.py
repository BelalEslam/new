from auth import Auth

def test_signup():
    auth = Auth()
    user_data = {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'testuser@example.com',
        'address': '123 Test Street',
        'name': 'Test User',
        'phone_number': '1234567890'
    }
    print("\nTesting Sign Up:")
    success, message = auth.signup(**user_data)
    print(f"Signup Result: {message}")

def test_login():
    auth = Auth()
    print("\nTesting Correct Login (by username):")
    success, message = auth.login('testuser', 'testpass123')
    print(f"Login Result: {message}")

    print("\nTesting Correct Login (by email):")
    success, message = auth.login('testuser@example.com', 'testpass123')
    print(f"Login Result: {message}")

    print("\nTesting Wrong Password:")
    success, message = auth.login('testuser', 'wrongpass')
    print(f"Login Result: {message}")

    print("\nTesting Non-existent User:")
    success, message = auth.login('not_a_user', 'password')
    print(f"Login Result: {message}")

if __name__ == "__main__":
    print("Starting Authentication Tests...")
    test_signup()
    test_login()
    print("\nAll tests completed!") 