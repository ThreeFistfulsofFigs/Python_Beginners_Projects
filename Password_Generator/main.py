# ============================================================================
# PASSWORD GENERATOR
# ============================================================================
# This script generates cryptographically secure passwords with customizable
# length and character types. It includes validation to ensure required character
# types are present and evaluates password strength based on complexity criteria.
# ============================================================================

# Import required libraries
import secrets  # For cryptographically secure random selection
import string   # For character sets (letters, digits, punctuation)
import re       # For regular expression pattern matching

# ============================================================================
# PASSWORD GENERATION AND VALIDATION CLASS
# ============================================================================
class Password:
    def __init__(self, length: int = 12, uppercase: bool = True, symbols: bool = True) -> None:
        """
        Initializes the Password generator with specified length and character type options.

        Args:
            length (int): Desired password length (default: 12)
            uppercase (bool): Include uppercase letters if True (default: True)
            symbols (bool): Include special characters if True (default: True)

        Returns:
            None: Sets up character set for password generation
        """
        # CONFIGURATION STORAGE
        # Store user-specified password parameters
        self.length = length
        self.use_uppercase = uppercase
        self.use_symbols = symbols

        # BASE CHARACTER SET
        # Start with lowercase letters and digits as minimum requirements
        self.base_characters: str = string.ascii_lowercase + string.digits

        # EXTEND CHARACTER SET
        # Add uppercase letters if specified
        if self.use_uppercase:
            self.base_characters += string.ascii_uppercase
        # Add symbols if specified
        if self.use_symbols:
            self.base_characters += string.punctuation

    def generate(self) -> str:
        """
        Generates a cryptographically secure password and ensures it meets character requirements.

        Returns:
            str: Generated password meeting all specified criteria
        """
        # PASSWORD GENERATION LOOP
        # Continue generating until validation criteria are met
        while True:
            # Generate password using list comprehension for efficiency
            password = ''.join(secrets.choice(self.base_characters) for _ in range(self.length))
            # Validate password meets character requirements
            if self._validate_password(password):
                return password

    def _validate_password(self, password: str) -> bool:
        """
        Validates that the password contains required character types based on configuration.

        Args:
            password (str): Password string to validate

        Returns:
            bool: True if password meets all requirements, False otherwise
        """
        # UPPERCASE VALIDATION
        # Check for at least one uppercase letter if use_uppercase is True
        if self.use_uppercase and not re.search(r"[A-Z]", password):
            return False

        # SYMBOL VALIDATION
        # Check for at least one symbol if use_symbols is True
        if self.use_symbols and not re.search(r"[^a-zA-Z0-9]", password):
            return False

        # VALIDATION SUCCESS
        # Return True if all checks pass
        return True

    def check_strength(self, password: str) -> tuple[str, int]:
        """
        Evaluates password strength based on length and character type diversity.

        Args:
            password (str): Password string to evaluate

        Returns:
            tuple[str, int]: Strength description and score (0-100)
        """
        # INITIALIZE SCORE
        # Start with zero and add points based on criteria
        score = 0
        strength = "Weak"

        # LENGTH SCORING
        # Award points based on password length
        if len(password) >= 12:
            score += 30
        elif len(password) >= 8:
            score += 15
        else:
            score += 5

        # CHARACTER TYPE SCORING
        # Add points for each character type present
        if re.search(r"[a-z]", password):
            score += 15  # Lowercase letters
        if re.search(r"[A-Z]", password):
            score += 15  # Uppercase letters
        if re.search(r"[0-9]", password):
            score += 15  # Digits
        if re.search(r"[^a-zA-Z0-9]", password):
            score += 15  # Symbols

        # COMPLEXITY BONUS
        # Extra points for long passwords with mixed characters
        if len(password) >= 16 and re.search(r"[a-zA-Z0-9[^a-zA-Z0-9]]", password):
            score += 10

        # STRENGTH CLASSIFICATION
        # Assign descriptive strength based on score
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Moderate"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"

        return strength, score

# ============================================================================
# MAIN PROGRAM LOGIC WITH OUTPUT DISPLAY
# ============================================================================
def main() -> None:
    """
    Main function to generate and display passwords with strength evaluation.

    Returns:
        None: Prints generated passwords with strength information
    """
    # PASSWORD GENERATOR INITIALIZATION
    # Create instance with specified length and character types
    password_generator: Password = Password(length=20, uppercase=True, symbols=True)

    # PASSWORD GENERATION LOOP
    # Generate and display 10 passwords with their strength
    for i in range(10):
        # Generate a single password
        generated: str = password_generator.generate()
        # Evaluate password strength
        strength, score = password_generator.check_strength(generated)

        # FORMATTED OUTPUT
        # Display password and its characteristics
        print('____________________________________')
        print(f'Password: {generated} ({len(generated)} characters)')
        print(f'Strength: {strength} (Score: {score}/100)')
        print('____________________________________')

# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    # Execute main function only when script is run directly
    main()