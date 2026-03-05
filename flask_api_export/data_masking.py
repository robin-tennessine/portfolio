"""
PDPA Data Masking Utilities
Masks sensitive personal data for compliance with Thailand's PDPA
"""

import re
import hashlib


class PDPAMasker:
    """Handles data masking for Personal Data Protection Act (PDPA) compliance"""

    @staticmethod
    def mask_name(name):
        """
        Mask person's name, showing only first character
        Example: "Somchai Phonpakdee" -> "S****** P*********"
        """
        if not name or not isinstance(name, str):
            return "***"

        words = name.strip().split()
        masked_words = []

        for word in words:
            if len(word) == 0:
                continue
            elif len(word) == 1:
                masked_words.append("*")
            else:
                masked_words.append(word[0] + "*" * (len(word) - 1))

        return " ".join(masked_words)

    @staticmethod
    def mask_id_card(id_card):
        """
        Mask Thai ID card number (13 digits)
        Example: "1234567890123" -> "1-2***-****-**-3"
        Show first 2 digits and last 1 digit only
        """
        if not id_card:
            return "***"

        # Remove all non-digit characters
        digits = re.sub(r'\D', '', str(id_card))

        if len(digits) != 13:
            return "***"

        # Thai ID format: X-XXXX-XXXXX-XX-X
        # Mask to: X-X***-*****-**-X
        return f"{digits[0]}-{digits[1]}***-*****-**-{digits[-1]}"

    @staticmethod
    def mask_passport(passport):
        """
        Mask passport number
        Example: "AB1234567" -> "AB****567"
        Show first 2 and last 3 characters
        """
        if not passport or not isinstance(passport, str):
            return "***"

        passport = passport.strip().upper()

        if len(passport) < 6:
            return "***"

        return passport[:2] + "*" * (len(passport) - 5) + passport[-3:]

    @staticmethod
    def mask_email(email):
        """
        Mask email address
        Example: "somchai@example.com" -> "s******@e******.com"
        """
        if not email or not isinstance(email, str) or '@' not in email:
            return "***@***.***"

        local, domain = email.split('@', 1)

        # Mask local part
        if len(local) <= 1:
            masked_local = "*"
        else:
            masked_local = local[0] + "*" * (len(local) - 1)

        # Mask domain
        if '.' in domain:
            domain_parts = domain.split('.')
            masked_domain_parts = []
            for part in domain_parts:
                if len(part) <= 1:
                    masked_domain_parts.append("*")
                else:
                    masked_domain_parts.append(part[0] + "*" * (len(part) - 1))
            masked_domain = ".".join(masked_domain_parts)
        else:
            masked_domain = domain[0] + "*" * (len(domain) - 1) if len(domain) > 1 else "*"

        return f"{masked_local}@{masked_domain}"

    @staticmethod
    def mask_phone(phone):
        """
        Mask phone number
        Example: "0812345678" -> "08****5678"
        Show first 2 and last 4 digits
        """
        if not phone:
            return "***"

        # Remove all non-digit characters
        digits = re.sub(r'\D', '', str(phone))

        if len(digits) < 7:
            return "***"

        if len(digits) == 10:  # Thai mobile format
            return f"{digits[:2]}****{digits[-4:]}"
        else:
            return f"{digits[:2]}****{digits[-4:]}"

    @staticmethod
    def generate_anonymous_id(original_id):
        """
        Generate consistent anonymous ID using hash
        Same input always produces same anonymous ID
        """
        if not original_id:
            return "ANON_UNKNOWN"

        # Use SHA256 hash and take first 8 characters
        hash_object = hashlib.sha256(str(original_id).encode())
        hash_hex = hash_object.hexdigest()
        return f"ANON_{hash_hex[:8].upper()}"

    @classmethod
    def mask_transaction_data(cls, data):
        """
        Mask all sensitive fields in transaction data dictionary
        """
        masked = data.copy()

        # Mask sensitive fields if they exist
        if 'customer_name' in masked:
            masked['customer_name'] = cls.mask_name(masked['customer_name'])

        if 'id_card' in masked:
            masked['id_card'] = cls.mask_id_card(masked['id_card'])

        if 'passport' in masked:
            masked['passport'] = cls.mask_passport(masked['passport'])

        if 'email' in masked:
            masked['email'] = cls.mask_email(masked['email'])

        if 'phone' in masked:
            masked['phone'] = cls.mask_phone(masked['phone'])

        # Generate anonymous ID if customer_id exists
        if 'customer_id' in masked:
            masked['anonymous_id'] = cls.generate_anonymous_id(masked['customer_id'])

        return masked


# Example usage and testing
if __name__ == "__main__":
    # Test data masking
    masker = PDPAMasker()

    print("=== PDPA Data Masking Examples ===\n")

    # Test name masking
    print("Name Masking:")
    print(f"  Original: Somchai Phonpakdee")
    print(f"  Masked:   {masker.mask_name('Somchai Phonpakdee')}\n")

    # Test ID card masking
    print("ID Card Masking:")
    print(f"  Original: 1234567890123")
    print(f"  Masked:   {masker.mask_id_card('1234567890123')}\n")

    # Test passport masking
    print("Passport Masking:")
    print(f"  Original: AB1234567")
    print(f"  Masked:   {masker.mask_passport('AB1234567')}\n")

    # Test email masking
    print("Email Masking:")
    print(f"  Original: somchai@example.com")
    print(f"  Masked:   {masker.mask_email('somchai@example.com')}\n")

    # Test phone masking
    print("Phone Masking:")
    print(f"  Original: 0812345678")
    print(f"  Masked:   {masker.mask_phone('0812345678')}\n")

    # Test anonymous ID generation
    print("Anonymous ID:")
    print(f"  Customer ID: CUST001")
    print(f"  Anonymous:   {masker.generate_anonymous_id('CUST001')}\n")

    # Test full transaction masking
    print("Full Transaction Masking:")
    transaction = {
        'transaction_id': 'TXN001',
        'customer_id': 'CUST001',
        'customer_name': 'Somchai Phonpakdee',
        'id_card': '1234567890123',
        'email': 'somchai@example.com',
        'phone': '0812345678',
        'amount': 1500.00,
        'product': 'iPhone 15 Pro'
    }

    masked = masker.mask_transaction_data(transaction)

    print("  Original:")
    for key, value in transaction.items():
        print(f"    {key}: {value}")

    print("\n  Masked:")
    for key, value in masked.items():
        print(f"    {key}: {value}")
