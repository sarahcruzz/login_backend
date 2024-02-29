[15:26] BRUNA NUNES LIMA DA CRUZ
import os
# possibilita a manipulação do servidor
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs
 
# biblioteca que cipritografa as senhas
import hashlib
 
# CRIAÇÃO DO SERVIDOR
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # Tenta abrir o arquivo idx.html
            f = open(os.path.join(path, 'login.html'), 'r')
            # Se existir, envia o conteúdo do arquivo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
 
        return super().list_directory(path)
   
 
    # CANAL DE COMUNICAÇÃO
    def do_GET(self):
        if self.path == '/login':
            # Tenta abrir o arquivo login.html
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found")
 
        # criação de rota para página de suscesso de login
        elif self.path == '/turmas':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()            
            self.wfile.write(content.encode('utf-8'))
 
        # criação de rota para página de suscesso de login
        elif self.path == '/usuario_cadastrado':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()            
            self.wfile.write(content.encode('utf-8'))
 
        # criação de rota para página de erro
        elif self.path == '/login_failed':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
 
                # Adiciona a mensagem de erro no conteúdo da página
            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
            self.wfile.write(content.encode('utf-8'))
 
        # criação do usuário não existente
        elif self.path.startswith('/cadastro'):
 
            # Extraindo os parâmetros da URL
            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login', [''])[0]
            senha = query_params.get('senha', [''])[0]
 
            # Mensagem de boas-vindas
            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro."
 
            # Responde ao cliente com a página de cadastro
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            # Lê o conteúdo da página cadastro.html
            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                content = cadastro_file.read()
 
            # Substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}', welcome_message)
 
            # Envia o conteúdo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))
            return  # Adicionando um return para evitar a execução do restante do código
       
        # criação de rota para página de suscesso do cadastro da turma
        elif self.path == '/cad_turma':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()            
            self.wfile.write(content.encode('utf-8'))
 
        # criação de rota para página de erro do cadastro de turma
        elif self.path == '/failed_turma':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'erro.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()            
            self.wfile.write(content.encode('utf-8'))
 
          # criação de rota para página de suscesso do cadastro da turma
        elif self.path == '/cad_ativ':
            # Responde ao cliente com a menssagem de login/senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            # Lê o conteúdo da página html
            with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()            
            self.wfile.write(content.encode('utf-8'))
 
        else:
            # Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()
 
    # FUNÇÕES PARA REAIZAR AS VALIDAÇÕES DE LOGIN
    def usuario_existente(self, login, senha):
        # Verifica se o login já existe no arquivo
        with open('dados.login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                    if login == stored_login:
                        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
                        print("cheguei aqui significando que localizei o login informado")
                        print("senha: " + senha)
                        print(" senha_armazenada: " + senha)
                        print(stored_senha_hash)
                        return senha_hash == stored_senha_hash
        return False
   
    # Funções para Login do Professor
    def adicionar_usuário(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()  
        with open('dados.login.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')
 
 
    def remover_ultima_linha(self, arquivo):
        print ("Vou excluir ultima linha")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])
 
    # Funções para Cadastro da Turma
    def turma_existente(self, id, turma):
        with open('dados_turma.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_id, stored_turma = line.strip().split(';')
                    if id == stored_id:
                        if turma == stored_turma:
                            return True
        return False
   
    def adicionar_turma(self, id, turma):
        with open('dados_turma.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{id};{turma}\n')
 
   
    # Funções para Cadastro da Atividade
    def atividade_existente(self, codigo, descricao):
        with open('atividades_turmas.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_codigo, stored_descricao = line.strip().split(';')
                    if codigo == stored_codigo:
                        if descricao == stored_descricao:
                            return True
        return False
   
    def adicionar_atividade(self, codigo, descricao):
        with open('atividades_turmas.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{codigo};{descricao}\n')
   
 
    # Captura dos dados do formulário através do 'action' inserir nor 'form'
    def do_POST(self):
        # Usuário logado com Sucesso
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)
 
            # Exibe os dados no terminal
            print("Dados do formulário:")
            print("Email:", form_data.get('email', [''])[0])
            print("Senha:", form_data.get('senha', [''])[0])
 
            # Verifica se o usuário já existe
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
 
            if self.usuario_existente(login, senha):
                # Responde ao cliente indicando que o usuário logou com sucesso
                self.send_response(302)
                self.send_header('Location', '/turmas')
                self.end_headers()
                # Adicionando um return para evitar a execução do restante do código
                return
       
            else:
                # Verifica se o login já existe no arquivo
                if any(line.startswith(f"{login};") for line in open('dados.login.txt', 'r', encoding='utf-8')):
                    # Redireciona o cliente para a rota "/login_failed"
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    # Adicionando um return para evitar a execução do restante do código
                    return
 
                else:
                    # Redireciona o cliente para a rota "/cadastro" com os dados de login e senha
                    self.adicionar_usuário(login, senha, nome='None')
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    # Adicionando um return para evitar a execução do restante do código
                    return  
 
 
        elif self.path.startswith('/confirmar_cadastro'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)
 
            #query_params = parse_qs(urlparse(self.path).query)
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
            nome = form_data.get('nome', [''])[0]
 
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
 
            # Verifica se o usuário já existe
            if self.usuario_existente(login, senha):
                # Atualiza o arquivo com o nome, se a senha estiver correta
                with open('dados.login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
 
                with open('dados.login.txt', 'w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha, stored_nome = line.strip().split(';')
                        print(stored_login, stored_senha, stored_nome)
 
                        if login == stored_login and senha_hash == stored_senha:
                            line = f"{login};{senha_hash};{nome}\n"
                        file.write(line)
 
                # Redireciona o cliente para onde desejar após a confirmação
                with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
 
            else:
                # Se o usuário não existe ou a senha está incorreta, redireciona para outra página
                self.remover_ultima_linha('dados.login.txt')
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("A senha não confere. Retome o procedimento!".encode('utf-8'))
 
 
        # CADASTRAR TURMA
        elif self.path == '/cad_turma':
            # Cadastra a turma se ela não existir
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)
 
            id = form_data.get('id', [''])[0]
            turma = form_data.get('turma', [''])[0]
 
            # Verifica se o valor está vazio e da erro
            if id.strip() == '' or turma.strip() == '':
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
       
            # Verifica se o usuário já existe
            elif self.turma_existente(id, turma) == True:
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
 
            # Adiciona a turma
            else:
                self.adicionar_turma(id, turma)
                self.send_response(302)
                self.send_header('Location', '/usuario_cadastrado')
                self.end_headers()
                return
           
 
        # CADASTRAR ATIVIDADE
        elif self.path == '/cad_ativ':
            # Cadastra a turma se ela não existir
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)
 
            codigo = form_data.get('codigo', [''])[0]
            descricao = form_data.get('descricao', [''])[0]
 
            print(codigo, descricao)
 
            # Verifica se o valor está vazio e da erro
            if codigo.strip() == '' or descricao.strip() == '':
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
       
            # Verifica se o usuário já existe
            elif self.atividade_existente(codigo, descricao) == True:
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
 
            # Adiciona a atividade
            else:
                self.adicionar_atividade(codigo, descricao)
                self.send_response(302)
                self.send_header('Location', '/usuario_cadastrado')
                self.end_headers()
                return
           
 
        else:
            # Se não for a rota "/enviar_login", continua com o comportamento padrão
            super(MyHandler, self).do_POST()
 
 
# Define o IP e a porta a serem utilizados
endereco_ip = "0.0.0.0"
porta = 8000
 
# Cria um servidor na porta e IP especificados
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciado em {endereco_ip}:{porta}")
    # Mantém o servidor em execução
    httpd.serve_forever()