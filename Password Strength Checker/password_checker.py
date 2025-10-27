import re

def check_password_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if re.search("[a-z]", password):
        strength += 1
    if re.search("[A-Z]", password):
        strength += 1
    if re.search("[0-9]", password):
        strength += 1
    if re.search("[@#$%^&*()_+!]", password):
        strength += 1

    if strength == 5:
        return "Strong 💪"
    elif strength >= 3:
        return "Moderate ⚠️"
    else:
        return "Weak ❌"

if __name__ == "__main__":
    print("Password Strength Checker")
    password = input("Enter your password: ")
    print("Your password strength is:", check_password_strength(password))
