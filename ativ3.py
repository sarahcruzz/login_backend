# Navega no diretorio
import os
# Manipula e Cria um servidir (sem framework)
from http.server import SimpleHTTPRequestHandler
# Gerencia a comunicação com o cliente
import socketserver
 
from urllib.parse import parse_qs
 
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
        if self.path =='/login.html':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                    self.send_response(200)
                    self.send_header("content-type","text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))          
        # Caso dê erro
            except FileNotFoundError:
                pass
        else:
            super().do_GET()

    def usuario_existente(self, login):
        #verifica se o login já existe no arquivo
        with open('dados_login.txt', 'r') as file:
            for line in file:
                stored_login, _ = line.strip().split(';')
                if login == stored_login:
                    return True
        return False
 
    def do_POST(self):
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            # Obtém o comprimento do corpo da requesição
            content_length = int(self.headers['content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados o formulário
            form_data = parse_qs(body)
 
            # Exibe os dados no terminal
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('senha', [''][0]))

            login = form_data.get('email', [''])[0]
            if self.usuario_existente(login):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                mensagem = f"Usuário {login} já consta em nossos registros"
                self.wfile.write(mensagem.encode('utf-8'))
            else:
                with open('dados_login.txt', 'a', encoding='utf-8') as file:
                    senha = form_data.get('senha', [''])[0]
                    file.write(f"{login};{senha}\n")

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; chrset=utf-8')
                    self.end_headers()
                    mensagem = "Dados recebidos e armazenados com sucesso!"
                    self.wfile.write(mensagem.encode('utf-8'))    


            with open('dados_login.txt', 'a') as file:
                login = form_data.get('email',[''])[0]
                senha = form_data.get('senha',[''])[0]
                file.write(f"{login}, {senha}\n")
 
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r') as sucesso_file:
                content = sucesso_file.read()
                self.wfile.write(content.encode('utf-8'))
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
    
