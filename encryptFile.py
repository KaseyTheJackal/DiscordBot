from cryptography.fernet import Fernet
from os.path import exists

key = Fernet.generate_key()

if not exists('token.txt'):
    print("Please create a token.txt file with your Discord bot's token in it")
    exit()
else:

    with open('filekey.key', 'wb') as filekey:
       filekey.write(key)

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    fernet = Fernet(key)

    with open('token.txt') as file:
        original = file.read()

    encrypted = fernet.encrypt(bytes(original,encoding='utf8'))

    with open('token.txt', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        print("token.txt has been encrypted and saved over itself. It is now ready to be used")