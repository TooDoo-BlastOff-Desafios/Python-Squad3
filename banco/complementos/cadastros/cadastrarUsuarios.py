from django.contrib.auth.models import User

from banco.models import Endereco, Usuario
class Cadastro():    

    def cadastroLogin(self, *dadosLogin):
        login = User(
            username = dadosLogin[0]            
        )
        login.set_password(dadosLogin[1])
        login.save()

        self.login = User.objects.get(username=dadosLogin[0])

    def cadastroUsuario(self, *dadosUsuario):
        usuario = Usuario(
            nome = dadosUsuario[0],
            cpf = dadosUsuario[1],
            login = self.login
        )
        usuario.save()

    def cadastroEndereco(self, *dadosEndereco):
        endereco = Endereco(
            pais = dadosEndereco[0],
            estado = dadosEndereco[1],
            cidade = dadosEndereco[2],
            rua = dadosEndereco[3],            
            usuario = self.login         
        )
        endereco.save()
