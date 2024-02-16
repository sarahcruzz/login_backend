# Navega no diretorio
import os
# Manipula e Cria um servidir (sem framework)
from http.server import SimpleHTTPRequestHandler
# Gerencia a comunicação com o cliente
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
 
# Criação de Classe com artificio de HTTP
class MyMandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Tenta o Código abaixo
        try:
            # Tenta abrir o arquivo index.html
            f = open(os.path.join(path, 'index.html'), 'r')
            # Se existir, envia o conteudo do arquivo
            # Envia para o Cliente o Código de Sucesso
            self.send_response(200)
            # Forma de Tratmento
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Leitura do HTML
            self.wfile.write(f.read().encode('utf-8'))
            # Finaliza para não contnuar o carregamento
            f.close
            return None
        # Caso dê erro
        except FileNotFoundError:
            pass
 
        return super().list_directory(path)
   
    def do_GET(self):
        if self.path =='/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          
        # Caso dê erro
            except FileNotFoundError:
                pass
           
        elif self.path == '/login_failed':
            # Responde ao cliente a mensagem de login/senha incorreta
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           
            # Lê o conteudo da pagina login.html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               
            # adiciona a mensagem de erro no conteudo da pagina
            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
            # Envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8')) 

        elif self.path.startswith('/cadastro'):
            # Extraindo os parâmetros da URL

            query_params = parse_qs(urlparse(self.path).query)   
            login = query_params.get('login', [''])[0]
            senha = query_params.get('senha', [''])[0]

            # Mensagem de boas-vindas

            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete seu cadastro"

            # Responde ao cliente com a página de cadastro
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:

                content = cadastro_file.read()

            # Substitui os marcadores de posição pelos valores correspondentes
                
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}', welcome_message)

            # Envia o conteúdo modificado para o cliente

            self.wfile.write(content.encode('utf-8'))

            return # Adicionando um return para evitar a execução do restante do código
        
        elif self.path.startswith('/tela_logada'):
    
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'tela_logada.html'), 'r', encoding='utf-8') as file:
                content = file.read()
                
                self.wfile.write(content.encode('utf-8'))
            
            return
        else:
            super().do_GET()
           
    def usuario_existente(self, login, senha):
        #verifica se o login já existe
        with open('dados.login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_login, stored_senha_hash, stored_name = line.strip().split(';')
                if login == stored_login:
                    senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
                    print(stored_senha_hash)
                    
                    return senha_hash == stored_senha_hash
                    
        return False
    
    def adicionar_usuario(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()

        with open('dados.login.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')    

    def remover_ultima_linha(self, arquivo):
        print("Vou excluir ultima linha")

        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])
 
    def do_POST(self):
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            # Obtém o comprimento do corpo da requesição
            content_length = int(self.headers['content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados o formulário
            form_data = parse_qs(body, keep_blank_values=True)

            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]

            # Exibe os dados no terminal
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", login)
            print("Senha:", senha)
           
            # Verifica se o usuario já existe

            if self.usuario_existente(login, senha):
                # responde ao cliente indicando que o usuario já consta nos registros
                self.send_response(302)
                self.send_header('Location', '/tela_logada')
                self.end_headers()
           
                return
            
            else:
                if any(line.startswith(f"{login};") for line in open("dados.login.txt", "r", encoding="UTF-8")):
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return # adicionando um return para evitar a execução
               
                else:
                    self.adicionar_usuario(login, senha, nome="None")
   
                    self.send_response(302)
                    self.send_header("Location", f"/cadastro?login={login}&senha={senha}")
                    self.end_headers()

                    return
        
        elif self.path.startswith('/confirmar_cadastro'):
            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')

            form_data = parse_qs(body, keep_blank_values=True)

            login = form_data.get('email', [''])[0]
            senha = form_data.get('conf_senha', [''])[0]
            nome = form_data.get('name', [''])[0]
            
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()

            if self.usuario_existente(login, senha):

                # Atualiza o arquivo com o nome, se a senha estiver correta

                with open('dados.login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                with open('dados.login.txt', 'w', encoding='utf-8') as file:

                    for line in lines:
                        stored_login, stored_senha, stored_name = line.strip().split(';')

                        print(stored_login, stored_name, stored_senha)

                        if login == stored_login and senha_hash == stored_senha:
                            line = f"{login};{senha_hash};{nome}\n"
                        
                        file.write(line)

                        # Redireciona o cliente para onde desejar após a confirmação
                        
                        self.send_response(302)
                        self.send_header('Location', '/tela_logada')
                        self.end_headers()

                        
                            # Se o usuário não existe ou a senha está incorreta, redireciona para outra página
                    else:
                        self.send_response(302)
                        self.send_header("Content-type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write("A senha não confere. Tente novamente!".encode("utf-8"))
                        return

            else:
                # Se não for a rota "/enviar_login", continua com o comportamento padrão
                super(MyMandler,self).do_POST()
 
 
# Define o IP  e a porta a serem utilizados
endereco_ip = "0.0.0.0"
porta = 8000
 
# Cria um servidor na porta e IP especificos
with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    # Mantém o servidor em execução
    httpd.serve_forever()