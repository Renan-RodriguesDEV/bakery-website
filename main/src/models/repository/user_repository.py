from typing import Literal

from src.utils.hasher import Hasher

from ...utils.uteis import Logger
from ..entities.database import Cliente, DatabaseHandler, User


class UserRepository(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def insert_user(
        self=None,
        username=None,
        password=None,
        cpf=None,
        telefone=None,
        email=None,
        type_user: Literal["Owner/Employee", "Client"] = "Client",
    ):
        with self:
            if type_user == "Owner/Employee":
                user = User(nome=username, senha=password)
                self.session.add(user)
                self.session.commit()
                return True
            elif type_user == "Client":
                user = Cliente(nome=username, cpf=cpf, telefone=telefone, email=email)
                self.session.add(user)
                self.session.commit()
                return True
        return False

    def select_user(
        self, username, type_user: Literal["Owner/Employee", "Client"] = "Client"
    ):
        with self:
            if type_user == "Owner/Employee":
                user = self.session.query(User).filter_by(nome=username).first()
                return user
            elif type_user == "Client":
                user = self.session.query(Cliente).filter_by(nome=username).first()
                return user
            return None

    def select_user_cpf(self, cpf):
        with self:
            return self.session.query(Cliente).filter_by(cpf=cpf).first()

    def select_all_users(self, type_user: Literal["Owner/Employee", "Client"]):
        with self:
            if type_user == "Owner/Employee":
                users = self.session.query(User).all()
                return users
            elif type_user == "Client":
                users = self.session.query(Cliente).all()
                return users
            return None

    def update_user(self, username, new_name, new_password):
        with self:
            try:
                user = self.session.query(User).filter_by(nome=username).first()
                user.senha = Hasher().hasherpswd(new_password)
                user.nome = new_name
                self.session.commit()
                return True
            except Exception as e:
                Logger.log_red(e)
                return False

    def delete_user(self, username, type_user: Literal["Owner/Employee", "Client"]):
        with self:
            try:
                if type_user == "Owner/Employee":
                    user = self.session.query(User).filter_by(nome=username).first()
                    self.session.delete(user)
                    self.session.commit()
                    return True
                elif type_user == "Client":
                    user = self.session.query(Cliente).filter_by(nome=username).first()
                    self.session.delete(user)
                    self.session.commit()
                    return True
            except Exception as e:
                Logger.log_red(e)
                return False
        return False
