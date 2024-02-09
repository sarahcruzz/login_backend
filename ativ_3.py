import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs

# Esta versão manin8 verifica se usuário já existe e se senha informada está correta
# Em caso de novo usuario, ou seja, um login que não está na base, ele é cadastrado na base e recebe uma mensgaem de boas vinadas


class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # Tenta abrir o arquivo idx.html
            f = open(os.path.join(path, 'idx.html'), 'r')
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

        elif self.path == '/login_failed':
            # Responde ao cliente com a mensagem de login/senha incorreta
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Lê o conteúdo da página login.html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()

            # Adiciona a mensagem de erro no conteúdo da página
            mensagem = "Login e/ou senha incorreta. Tente novamente."
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message"><p>{mensagem}</p></div>')

            # Envia o conteúdo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))

        else:
            # Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
        # Verifica se o login já existe no arquivo

        with open('dados_login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                stored_login, stored_senha = line.strip().split(', ')

                if login == stored_login:
                    print ("cheguei aqui significando que localizei o login informado")
                    print ("senha: " + senha)
                    print(" senha_armazenada: " + senha)
                    return senha == stored_senha
        return False

    def do_POST(self):
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            # Obtém o comprimento do corpo da requisição
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
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                mensagem = f"Usuário {login} logado com sucesso!!!"
                
                with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r', encoding='utf-8') as sucesso_file:
                    content = sucesso_file.read()
                self.wfile.write(content.encode('utf-8'))
                
            else:
                # Verifica se o login já existe no arquivo
                if any(line.startswith(f"{login}, ") for line in open('dados_login.txt', 'r', encoding='utf-8')):
                    # Redireciona o cliente para a rota "/login_failed"
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return  # Adicionando um return para evitar a execução do restante do código
                else:
                    # Adiciona o novo usuário ao arquivo
                    with open('dados_login.txt', 'a', encoding='utf-8') as file:
                        file.write(f"{login};{senha}\n")

                    # Responde ao cliente com a mensagem de boas-vindas
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    mensagem = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui."
                    self.wfile.write(mensagem.encode('utf-8'))
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
