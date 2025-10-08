"""caesar"""
UPPER="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DOWN="abcdefghijklmnopqrstuvwxyz"
def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i in UPPER:
            if 97 > ord(i)+shift >90:
                ciphertext+=chr(ord(i)+shift-26)
            else:
                ciphertext+=chr(ord(i)+shift)
        elif i in DOWN:
            if ord(i)+shift>122:
                ciphertext+=chr(ord(i)+shift-26)
            else:
                ciphertext+=chr(ord(i)+shift)
        else:
            ciphertext+=i

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i in UPPER:
            if ord(i)-shift < 65:
                plaintext+=chr(ord(i)-shift+26)
            else:
                plaintext+=chr(ord(i)-shift)
        elif i in DOWN:
            if 97 > ord(i)-shift > 90:
                plaintext+=chr(ord(i)-shift+26)
            else:
                plaintext+=chr(ord(i)-shift)
        else:
            plaintext+=i

    return plaintext
