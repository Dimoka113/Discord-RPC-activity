import os
from functions.gateway import Gateway
from functions.logger import Logger

class Client(Gateway):
    id = None
    p = "data/.client"
    logger = None

    def __init__(self, path, logger = Logger("Client")):
        super().__init__(path, Logger("Gateway-Client"))

        if not os.path.exists("data/.client"):
            _id = self.read()
            if _id == "0000000000000000000":
                logger.crit("Please enter your Client_ID in data/client_id.json")
                logger.warn("After the next run (if you specify it), it will be removed from the source file.")
                input("Press Enter to exit")
                os._exit(0)

            self.id = self.code(_id)
            open(self.p, "w+").write(self.id)
            logger.warn("The client_id was saved, and the original file in client_id.json was overwritten with zeros.")
            logger.info("If you need to specify a different client_id, delete the file: data/.client")
            self.write("0000000000000000000")
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