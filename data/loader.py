import os
from functions.gateway import Gateway
from functions.logger import Logger

class Client(Gateway):
    id = None
    p = "data/.client"
    logger = None

    def __init__(self, logger = Logger("Client")):

        if not os.path.exists("data/.client"):
            logger.crit("Please enter your Client_ID:")
            key = input("Client_ID: ")

            self.id = self.code(key)
            open(self.p, "w+").write(self.id)
            logger.warn("The client_id was saved.")
            logger.info("If you need to specify a different client_id, delete the file: data/.client")
        else:
            self.id = str(open(self.p, "r").read())

    def code(self, data: str) -> str:
        result = 0
        for char in data: result = result * 113 + ord(char)
        return str(hex(result))

    def decode(self, data: str) -> str:
        chars = []
        n = int(data, 16)
        while n > 0: chars.append(chr(n % 113)); n //= 113
        return ''.join(reversed(chars))