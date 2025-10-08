"""vigenre"""
upper={}
down={}
for j, upp in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    upper.update({upp: j})
for j, dow in enumerate("abcdefghijklmnopqrstuvwxyz"):
    down.update({dow: j})



def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    if keyword == "":
        raise ValueError("строка ключа не может быть пустой")
    k = 0
    while len(keyword)<len(plaintext):
        keyword+=keyword[k]
        k+=1
    ciphertext = ""
    for i, letter in enumerate(plaintext):
        if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            shift = upper[keyword[i]]
            if ord(letter)+ shift > 90:
                ciphertext+=chr(ord(letter)+shift-26)
            else:
                ciphertext+=chr(ord(letter)+shift)
        elif letter in "abcdefghijklmnopqrstuvwxyz":
            shift = down[letter]
            if ord(letter)+shift>122:
                ciphertext+=chr(ord(letter)+shift-26)
            else:
                ciphertext+=chr(ord(letter)+shift)
        else:
            ciphertext+=letter
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    if keyword == "":
        raise ValueError("строка ключа не может быть пустой")
    k = 0
    while len(keyword)<len(ciphertext):
        keyword+=keyword[k]
        k+=1
    plaintext = ""
    for i, letter in enumerate(ciphertext):
        if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            shift = upper[keyword[i]]
            if ord(letter)-shift < 65:
                plaintext+=chr(ord(letter)-shift+26)
            else:
                plaintext+=chr(ord(letter)-shift)
        elif letter in "abcdefghijklmnopqrstuvwxyz":
            shift = down[keyword[i]]
            if 97 > ord(letter)-shift:
                plaintext+=chr(ord(letter)-shift+26)
            else:
                plaintext+=chr(ord(letter)-shift)
        else:
            plaintext+=letter
    return plaintext
