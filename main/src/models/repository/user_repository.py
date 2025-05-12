from typing import Literal

from src.utils.hasher import Hasher

from ...utils.uteis import Logger, str_as_number
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
        type_user: Literal["Proprietario/Funcionario", "Cliente"] = "Cliente",
    ):
        with self:
            if type_user == "Proprietario/Funcionario":
                user = User(nome=username, senha=password)
                self.session.add(user)
                self.session.commit()
                return True
            elif type_user == "Cliente":
                password = password if password else cpf
                user = Cliente(
                    nome=username,
                    cpf=cpf,
                    telefone=telefone,
                    email=email,
                    senha=password,
                )
                self.session.add(user)
                self.session.commit()
                return True
        return False

    def select_user(
        self,
        username,
        type_user: Literal["Proprietario/Funcionario", "Cliente"] = "Cliente",
    ):
        with self:
            if type_user == "Proprietario/Funcionario":
                user = (
                    self.session.query(User)
                    .filter((User.email == username) | (User.nome == username))
                    .first()
                )
                if user:
                    Logger.sucess(f"Usuario encontrado: {user.nome}")
                    return user
            elif type_user == "Cliente":
                user = (
                    self.session.query(Cliente)
                    .filter((Cliente.nome == username) | (Cliente.email == username))
                    .first()
                )
                if user:
                    Logger.sucess(f"Usuario encontrado: {user.nome}")
                    return user
            return None

    def select_user_by_email(
        self,
        user_email,
        type_user: Literal["Proprietario/Funcionario", "Cliente"] = "Cliente",
    ):
        with self:
            if type_user == "Proprietario/Funcionario":
                user = self.session.query(User).filter(User.email == user_email).first()
                if user:
                    Logger.sucess(f"Usuario encontrado: {user.nome}")
                    return user
            elif type_user == "Cliente":
                user = (
                    self.session.query(Cliente)
                    .filter(Cliente.email == user_email)
                    .first()
                )
                if user:
                    Logger.sucess(f"Usuario encontrado: {user.nome}")
                    return user
            return None

    def select_user_cpf(self, cpf):
        with self:
            return self.session.query(Cliente).filter_by(cpf=cpf).first()

    def select_all_users(
        self, type_user: Literal["Proprietario/Funcionario", "Cliente"]
    ):
        with self:
            if type_user == "Proprietario/Funcionario":
                users = self.session.query(User).all()
                return users
            elif type_user == "Cliente":
                users = self.session.query(Cliente).all()
                return users
            return None

    def update_user(
        self,
        username=None,
        new_name=None,
        new_password=None,
        new_email=None,
        new_cpf=None,
        new_telefone=None,
        type_user: Literal["Proprietario/Funcionario", "Cliente"] = "Cliente",
    ):
        with self:
            try:
                if type_user == "Proprietario/Funcionario":
                    user = (
                        self.session.query(User)
                        .filter((User.nome == username) | (User.email == username))
                        .first()
                    )
                else:
                    user = (
                        self.session.query(Cliente)
                        .filter(
                            (Cliente.nome == username) | (Cliente.email == username)
                        )
                        .first()
                    )
                if new_password:
                    user.senha = Hasher().hasherpswd(new_password)

                if new_name:
                    user.nome = new_name

                if new_telefone:
                    user.telefone = str_as_number(new_telefone)

                if new_email:
                    user.email = new_email
                if new_cpf:
                    user.cpf = str_as_number(new_cpf)

                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def delete_user(
        self, username, type_user: Literal["Proprietario/Funcionario", "Cliente"]
    ):
        with self:
            try:
                if type_user == "Proprietario/Funcionario":
                    user = self.session.query(User).filter_by(email=username).first()
                    self.session.delete(user)
                    self.session.commit()
                    return True
                elif type_user == "Cliente":
                    user = self.session.query(Cliente).filter_by(nome=username).first()
                    self.session.delete(user)
                    self.session.commit()
                    return True
            except Exception as e:
                Logger.error(e)
                return False
        return False

    def reset_password(
        self,
        username,
        new_password,
        type_user: Literal["Proprietario/Funcionario", "Cliente"],
    ):
        with self:
            try:
                if type_user == "Proprietario/Funcionario":
                    user = self.session.query(User).filter_by(email=username).first()
                    user.senha = Hasher().hasherpswd(new_password)
                else:
                    user = self.session.query(Cliente).filter_by(email=username).first()
                    user.senha = Hasher().hasherpswd(new_password)
                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def get_token(self):
        with self:
            user = self.session.query(Cliente).first()
            if user:
                return user.token

    def set_token(self, token):
        with self:
            user = self.session.query(Cliente).first()
            user.token = token
            self.session.commit()
            return True
        return False
