import os
from cryptography.fernet import Fernet

csv_encryption_key = os.environ.get("csv_encryption_key")

def encrypt_file(file_name, encrypted_file_name):
    
    fernet = Fernet(csv_encryption_key)
    
    with open(file_name, 'rb') as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    with open(encrypted_file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        
        
def decrypt_file(file_name):
	fernet = Fernet(csv_encryption_key)
	
	with open(file_name, 'rb') as enc_file:
		encrypted = enc_file.read()
	
	decrypted = fernet.decrypt(encrypted)
 
	new_file_name = file_name.replace('encrypted', 'decrypted')
	
	with open(new_file_name, 'wb') as dec_file:
		dec_file.write(decrypted)