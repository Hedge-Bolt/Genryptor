from django.shortcuts import render
import random
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import cryptography
import time

# Create your views here.
def home(request):
    if request.method == 'POST':
        # Chooses random characters from the char_list to the lengh required by the user
        char_list = list('qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM1234567890!@#$%&*+-/=?^_`{|}~')

        passwd_length = request.POST['passwd_len']
        length = int(passwd_length)  
        passwd_list = random.choices(char_list,k = length)
        # Joins the characters in the password list to generate the final password 

        passwd = ''.join(passwd_list)

        return render(request, 'home.html', context={'passwd':passwd})
    
    return render(request, 'home.html')
    

def encryptor(request):
    if request.method == 'POST':

        # Takes the private/personal key of the user to encrypt the password
        pvt_key = request.POST['secret-key']

        
        # Converts user's Password into byt format
        key_bytes = pvt_key.encode()

        # Algo to Convert a string to 32 url-safe base64-encoded byte
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, iterations=100000, backend=default_backend(), salt=b'')

        # Generates a 32 url-safe base64-encoded byte of user's key
        pub_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        

        # Takes string(Password) to encrypt
        password = request.POST['passwd']

        #converts the string to bytes format
        password_bytes = password.encode()

        # Generates the final key to encrypt user's string(Password)
        f = Fernet(pub_key)
        # Encrypts string and give it in bytes format
        encryption_bytes = f.encrypt(password_bytes)
        # Decodes the encrypted string to normal chars and gives out final encryption
        encryption = encryption_bytes.decode()

        return render(request, 'encrypt.html', context = {'encryption': encryption})
    return render(request, 'encrypt.html')

def decryptor(request):
    if request.method == 'POST':
        try:
            # Takes the private key from user
            pvt_key = request.POST['secret-key']
        
            # Converts user's private key to bytes format
            key_bytes = pvt_key.encode()

            # Algo to Convert a string to 32 url-safe base64-encoded byte
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, iterations=100000, backend=default_backend(), salt=b'')

            # Generates a 32 url-safe base64-encoded byte of user's key
            pub_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))

            # Takes user's encryption 
            encryption = request.POST['passwd']


            # Generates the final key by using user's private key to decrypt user's string(Password)
            f = Fernet(pub_key)

            # Decrypts string and give it in bytes format
            decrypt = f.decrypt(encryption)

            # Decodes the decrypted string to normal chars and gives out users password
            org_passwd = decrypt.decode()

            return render(request, 'decrypt.html', {'org_passwd':org_passwd})

        
        except (cryptography.fernet.InvalidToken, TypeError):
            

            return render(request, 'decrypt.html', {'org_passwd':'Either your Encryption or your Secret key was wrong. Please try again.'})
    
    return render(request, 'decrypt.html')
    