import bcrypt


class Hasher:
    def hasherpswd(self, password, rounds=12):
        salt = bcrypt.gensalt(rounds=rounds)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode()

    def checkpswd(self, password, hashed):
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
