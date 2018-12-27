import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Decryptor(object):

    pass_state = None
    salt_state = None

    def __init__(self):
        pass

    def state_pw(self, pw, salt):

        Decryptor.pass_state = pw
        Decryptor.salt_state = salt

    def state_dec(self, priv):

        return self.decrypt(priv, Decryptor.pass_state, Decryptor.salt_state)

    def encrypt(self, priv, passwd, saltt):

        password = passwd  # b" #(input("pass?"))
        password = password.encode()
        salt = saltt  # b" #os.urandom(16)
        # salt = (input("salt?"))
        salt = salt.encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        cipher_suite = Fernet(key)

        priv = cipher_suite.encrypt(bytes(priv, 'utf-8'))

        return priv.decode("utf-8")

    def decrypt(self, pub, priv, passwd, saltt):
        password = passwd  # b"kiran0 #(input("pass?"))
        password = password.encode()
        salt = saltt  # b"salt0 #os.urandom(16)
        # salt = (input("salt?"))
        salt = salt.encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        cipher_suite = Fernet(key)

        pub_decy = bytes(pub, 'utf-8')  # cipher_suite.encrypt(pub)
        priv_decy = bytes(priv, 'utf-8')  # cipher_suite.encrypt(priv)

        pub_str = cipher_suite.decrypt(pub_decy)
        priv_str = cipher_suite.decrypt(priv_decy)

        # print (pub_str)
        # print (priv_str)

        returner = [pub_str, priv_str]

        return returner


if __name__ == '__main__':

    # test stuff here
    decry = Decryptor()
