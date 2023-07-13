from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import MD5

class CCrypt:
    def __get_digest(value: str):
        h = MD5.new()
        h.update(value.encode())
        return h.digest()

    def encode(message: str, passphrase: str):
        message = message.encode()
        key = CCrypt.__get_digest(passphrase)
        cipher = AES.new(key, AES.MODE_CFB)
        iv = cipher.iv
        ciphertext = cipher.encrypt(message)
        return b64encode(iv + ciphertext).decode('utf-8')
    def decode(data: str, passphrase: str):
        try:
            key = CCrypt.__get_digest(passphrase)
            data = b64decode(data.encode('utf-8'))
            iv = data[:AES.block_size]
            ciphertext = data[AES.block_size:]
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            msg = cipher.decrypt(ciphertext).decode()
            return True, msg
        except (ValueError, KeyError):
            return False, "Incorrect key"
        except Exception as e:
            return False, "Something went wrong"

        

if __name__ == '__main__':
    msg = "message tiếng việt"
    pw = "pw tiếng việt"

    res = CCrypt.encode(msg, pw)
    print(f'Encrypted text: {res}')
    print(CCrypt.decode(res, pw))
    print(CCrypt.decode(res, "pw sai"))