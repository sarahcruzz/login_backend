# Navega no diretorio
import os
# Manipula e Cria um servidir (sem framework)
from http.server import SimpleHTTPRequestHandler
# Gerencia a comunicação com o cliente
import socketserver
from urllib.parse import parse_qs, urlparse

import hashlib


# Criação de Classe com artificio de HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Tenta o Código abaixo
        try:
            # Abre o arquivo index.html
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                # Envia o cabeçalho HTTP
                # Se existir, envia o conteudo do arquivo
                # Envia para o Cliente o Código de Sucesso
                self.send_response(200)
                 # Forma de Tratmento
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Lê e envia o conteúdo do arquivo
                content = f.read()
                # Leitura do HTML
                self.wfile.write(content.encode('utf-8'))
                # Finaliza para não contnuar o carregamento
                f.close
                return None
            
        # Caso dê erro  
        except FileNotFoundError:
            pass

        return super().list_directory(path)
    
    def adicionar_turma(self, turma, descricao):
        print("Ad turma")
        print(turma)
        print(descricao)

        with open('cad_turma.txt', 'a', encoding='UTF-8') as turma:
            turma.write(f'{turma};{descricao}\n')

    def turma_existente(self, turma, descricao):
        with open('cad_turma.txt', 'r', encoding='utf-8') as file_turma:
            for line in file_turma:
                if line.strip():
                    stored_codigo, stored_descricao = line.strip().split(';')
                    if turma == stored_codigo:
                        print("Turma localizada")
                        return turma == stored_codigo
        return False
    
    def do_GET(self):
        if self.path == '/login':
            #Tentar abrir o arquivo login
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()# le o contedo do arquivo login 
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página
            # Caso dê erro
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        elif self.path == '/login_failed':
            #responde ao cliente com a mensagem de login/senha incorreta 
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            #le o conteud da página login.html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
            
            #Adiciona a mensagem de erro no conteúdo da página
                mensagem = 'Login e/ou senha incorretos. Tente novamente'
                content = content.replace('<!--Mensagem de erro inserida aqui-->', 
                                          f'<div class="error-message">{mensagem}</div>' )

            #Envia o conteudo modificado para o cliente 
            self.wfile.write(content.encode('utf-8')) 

        elif self.path.startswith('/cadastro'):
                query_params = parse_qs(urlparse(self.path).query)
                login = query_params.get('login', [''])[0]
                senha = query_params.get('senha', [''])[0]

                #mensagem de boas vindas 
                welcome_message= f'Olá {login}, seja bem-vendo! Percebemos que você é novo por aqui. Complete o seu Cadastro.'

                #Responde ao cliente com a página de cadastro
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                    content=cadastro_file.read()
                
                content = content.replace('{login}', login)
                content = content.replace('{senha}', senha)
                content = content.replace('{welcome_message}', welcome_message)

                self.wfile.write(content.encode('utf-8'))

                return     
        elif self.path == '/cad_turma':
            try:
                with open(os.path.join(os.getcwd(), 'turma.html'), 'r', encoding='utf-8') as codTurma:
                    content = codTurma.read() 
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'File not found')

        else:
            #Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
            # Verifica se o login já existe no arquivo

            with open('dados_login.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                        if login == stored_login:

                            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                            print('usuário existente')
                            print("cheguei aqui significando que localizei o login informado")
                            print("senha: " + senha)
                            print(" senha_armazenada: " + senha)
                            print(stored_senha_hash)
                            return senha_hash == stored_senha_hash
            return False
    
    def adicionar_usuario(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        with open('dados_login.txt', 'a', encoding='utf-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')
    
    def remover_ultima_linha(self, arquivo):
        print('Vou excluir a última linha')
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines =file.readlines()
        with open (arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])

    def do_POST(self):

        if self.path == '/cad_turma':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)

            turma = form_data.get('turma', [''])[0]
            descricao = form_data.get('descricao', [''])[0]
            
            if self.turma_existente(turma, descricao):
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Já temos essa turma cadastrada!!".encode('utf-8'))
            else:
                self.adicionar_turma(turma, descricao)
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Registro Novo!!".encode('utf-8'))
                return
            super().do_POST()

        #verifica se a rota é "/enviar_login" (isso tem que estar no action do formulario )
        elif self.path == '/enviar_login':
            #Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])

            #Lê o corpo de requisição
            body = self.rfile.read(content_length).decode('utf-8')

            #Parseia os dados do formulário 
            form_data = parse_qs(body, keep_blank_values=True)

            #Exibe os dados no terminal 
            print("Dados Formulário:")
            print("Email:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('senha', [''][0]))

            #verificar se o usuáro já existe:
            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]

            if self.usuario_existente(login, senha):
                #Responde ao cliente indicando que usuário já consta nos registros
                with open(os.path.join(os.getcwd(), 'turma.html'), 'r', encoding='utf-8') as usuario_existente_file:
                    content = usuario_existente_file.read() # le o contedo do arquivo login 

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            else:

                if any(line.startswith(f'{login};') for line in open('dados_login.txt', 'r', encoding='utf-8')):
                    #redireciona o cliente para a rota '/login_failed'
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return #Adicionando um return para evitar a execução do restante do código

                else:
                    #Armazena os dados num arquivo txt
                    # with open('dados_login.txt', 'a', encoding='utf-8') as file:
                        # login = form_data.get('email', [''])[0]
                        # senha = form_data.get('senha', [''])[0]
                        # file.write(f'{login};{senha};' + 'none' + '\n')

                        #redirecionando o cliente para a rota /cadastro com os dados de login e senha 

                        self.adicionar_usuario(login, senha, nome='None')
                        self.send_response(302)
                        self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                        self.end_headers()
                        return

                    # with open(os.path.join(os.getcwd(), 'resposta.html'), 'r', encoding='utf-8') as resposta_file:
                    #         content = resposta_file.read() # le o contedo do arquivo login 

                    # #Responde ao cliente indicando que os dados foram recebidos e armazenados com sucesso
                    # self.send_response(200)
                    # self.send_header("Content-type", "text/html; charset=utf-8")
                    # self.end_headers()
                    # self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página
                
        elif self.path.startswith('/confirmar_cadastro'):
            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')

            form_data = parse_qs(body, keep_blank_values=True)

            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
            nome = form_data.get('nome', [''])[0]
            
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()

            if self.usuario_existente(login, senha):

                with open('dados_login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                with open('dados_login.txt', 'w', encoding='utf-8') as file:

                    for line in lines:
                        stored_login, stored_senha, stored_name = line.strip().split(';')

                        print(stored_login, stored_name, stored_senha)

                        if login == stored_login and senha_hash == stored_senha:
                            line = f"{login};{senha_hash};{nome}\n"
                        
                        file.write(line)
                        
                        self.send_response(302)
                        self.send_header('Location', '/cad_turma')

                        # self.send_header('Content-type', 'text/html; charset=utf-8')    
                        # with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r', encoding='utf-8') as usuario_existente_file:
                        #     content = usuario_existente_file.read() # le o contedo do arquivo login 
                        self.end_headers()
                    
                    else:

                        self.send_response(302)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.end_headers()
                        self.wfile.write('A senha não confere. Retome o procedimento!'.encode('utf-8'))

                        return
        else:

            # Se não for a rota definida, conrinua com o comportamento padrão

            super(MyHandler, self).do_POST()

endereco_ip = "0.0.0.0"
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()

