import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
from banco import conectar
 
conexao = conectar()
 
# Criação de Classe com artificio de HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
   
        try:
           
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
               
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                content = f.read()
                self.wfile.write(content.encode('utf-8'))
                f.close
                return None
           
        except FileNotFoundError:
            print("Page is not fond")
 
        return super().list_directory(path)
   
 
    def do_GET(self):
 
        # Rota login
        if self.path == '/login':
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
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
           
 
                mensagem = 'Login e/ou senha incorretos. Tente novamente'
                content = content.replace('<!--Mensagem de erro inserida aqui-->',
                                          f'<div class="error-message">{mensagem}</div>' )
 
            #Envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))
 
        elif self.path.startswith('/cadastro'):
                query_params = parse_qs(urlparse(self.path).query)
                login = query_params.get('login', [''])[0]
                senha = query_params.get('senha', [''])[0]
 
 
                welcome_message= f'Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu Cadastro.'
 
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
 
        elif self.path.startswith('/cadastrar_turma'):
             self.send_response(200)
             self.send_header("content-type", "text/html; charset=utf-8")
             self.end_headers()
 
             with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as file:
                content = file.read()
               
                self.wfile.write(content.encode('utf-8'))
               
                return
       
        elif self.path.startswith('/cadastrar_atividade'):
             self.send_response(200)
             self.send_header("content-type", "text/html; charset=utf-8")
             self.end_headers()
 
             with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as file:
                content = file.read()
               
                self.wfile.write(content.encode('utf-8'))
               
                return
 
        else:
 
            super().do_GET()
 
    def usuario_existente(self, login, senha):
            cursor = conexao.cursor()
            cursor.execute("SELECT senha FROM dados_login WHERE login = %s", (login,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                return senha_hash == resultado[0]
            return False
   
    def turma_existente(self, descricao):
        # Vericação se a turma já existe
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        else:
            return False        # with open('dados_turma.txt', 'r', encoding='utf-8') as file:
        #     for line in file:
        #         if line.strip():
        #             stored_cod, stored_descricao = line.strip().split(";")
 
        #             if cod_turma == stored_cod or descricao == stored_descricao:
        #                 return True
       
   
    def atividade_existente(self,  descricao):
        # Vericação se a turma já existe
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        else:
            return False  
   
    def adicionar_usuario(self, login, senha, nome):
        cursor = conexao.cursor()
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO dados_login (login,senha,nome) VALUES (%s,%s,%s)", (login,senha_hash,nome))
        conexao.commit()
        cursor.close()
        # with open('dados.login.txt', 'a', encoding='utf-8') as file:
        #     file.write(f'{login};{senha_hash};{nome}\n')
 
    def adicionar_turma(self,  descricao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas ( descricao) VALUES (%s)", (descricao,))
        conexao.commit()
        cursor.close()
        # with open('dados_turma.txt', 'a', encoding='utf-8') as file:
        #     file.write(f'{cod_turma};{descricao}\n')
 
    def adicionar_atividade(self, descricao):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividades ( descricao) VALUES (%s)", (descricao,))
        conexao.commit()
        cursor.close()
        # with open('dados_atividade.txt', 'a', encoding='utf-8') as file:
        #     file.write(f'{cod_atividade};{descricao}\n')
   
    def remover_ultima_linha(self, arquivo):
        print('Vou excluir a última linha')
        with open(arquivo, 'r', encoding='urf-8') as file:
            lines =file.readlines()
        with open (arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])
 
    def adicionar_turma_professor(self, descTurma, id_professor):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas (descricao) VALUES (%s)", (descTurma,))
        cursor.execute("SELECT id_turma FROM turmas WHERE descricao = %s", (descTurma,))
        resultado = cursor.fetchone()
        cursor.execute("INSERT INTO turmas_professor (id_turma, id_professor) VALUES (%s, %s)", (resultado[0], id_professor))
        conexao.commit()
        cursor.close()

    def carrega_turmas_professor(self, login):
        # carrega turmas do professor
        cursor = conexao.cursor()
        cursor.execute("SELECT id_professor, nome FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        # resultado[0] trás o id_professor e resultado [1] trás o nome do professor
        id_professor = resultado[0]
        
        #código para obter turmas do professor
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT turmas.id_turma, turmas.descricao FROM turmas_professor INNER JOIN turmas"
            "ON turmas_professor.id_turma = turmas.id_turma WHERE turmas_professor.id_professor = %s", (id_professor,))
        turmas = cursor.fetchall()
        cursor.close()

        # construindo dinamicamente as linhas da tabela com as turmas do professor
        linhas_tabela = ""
        for turma in turmas:
            id_turma = turma[0]
            descricao_turma = turma[1]
            link_atividade = "<img src='icnatividade2.png'/>"
            linha = "<tr> <td style='text-align:center'>{}</td> <td style='text-align:center'>{}</td> </tr>".format(descricao_turma, link_atividade)
            linhas_tabela += linha

        with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as cad_turma_file:
            content = cad_turma_file.read()

            content = content.replace('{nome_professor}', resultado[1])
            content = content.replace('{id_professor}', str(id_professor))
            content = content.replace('{login}', str(login))

        # Substituindo o marcador de posição pelas linhas da tabela
        content = content.replace('<!-- Tabela com linhas zebradas -->', linhas_tabela)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(content.encode('utf-8'))



    def do_POST(self):
        #verifica se a rota é "/enviar_login" (isso tem que estar no action do formulario )
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])
 
            body = self.rfile.read(content_length).decode('utf-8')
 
            form_data = parse_qs(body, keep_blank_values=True)
 
            print("Dados Formulário:")
            print("Email:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('senha', [''][0]))
 
            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]
 
            if self.usuario_existente(login, senha):
                self.carrega_turmas_professor(login)
 
            else:
                cursor = conexao.cursor()
                cursor.execute("SELECT login FROM dados_login WHERE login = %s",(login,))
                resultado = cursor.fetchone()
                print("Sarah: " , resultado)
                #if any(line.startswith(f'{login};') for line in open('dados.login.txt', 'r', encoding='utf-8')):

                if resultado:
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    cursor.close()
                    return
 
                else:
                    #Armazena os dados num arquivo txt
                        #redirecionando o cliente para a rota /cadastro com os dados de login e senha
                    # self.adicionar_usuario(login, senha, nome='None')
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    return
 
        elif self.path.startswith('/confirmar_cadastro'):
 
            content_length= int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data=parse_qs(body, keep_blank_values=True)
 
            login = form_data.get('login', [''])[0]
            senha = form_data.get('senha', [''])[0]
            nome = form_data.get('nome', [''])[0]
 
            self.adicionar_usuario(login,senha,nome)
 
            self.send_response(302)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('Registro recebido com sucesso!'.encode('utf-8'))
           
        elif self.path.startswith('/cadastrar_turma'):
            content_length =  int(self.headers['content-length'])
            body= self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)
            descTurma = form_data.get('descturma', [''])[0]
            id_professor = form_data.get('id_professor', [''])[0]
            login = form_data.get('login', [''])[0]

            print(f"Cad_turma, dados do formulário {descTurma}{id_professor}")
            self.adicionar_turma_professor(descTurma, id_professor)
            self.carrega_turmas_professor(login)
 
            if cod_turma.strip()== '' or descricao.strip() == '':
                mensagem_erro = "Os campos não foram preenchidos corretamente, tente novamente."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
           
            elif self.turma_existente(descricao) == True:
                # self.send_response(302)  
                # self.send_header("Location", "/cadastro_turma_failed")
                # self.end_headers
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Turma já cadastrada, tente novamente com outros dados.".encode('utf-8'))
               
                mensagem_erro = "Turma já cadastrada, tente novamente com outros dados."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
           
            else:
                self.adicionar_turma(descricao)
                # Se os campos estiverem preenchidos, adiciona a turma
                # self.adicionar_turma(cod_turma, descricao)
 
                # self.send_response(302)
                # self.send_header("Location", "/cadastrar_turma")
                # self.end_headers()
 
                mensagem_erro = "Turma cadastrada com sucesso!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
 
        elif self.path.startswith('/cadastrar_atividade'):
            content_length =  int(self.headers['content-length'])
 
            body= self.rfile.read(content_length).decode('utf-8')
 
            from_data = parse_qs(body, keep_blank_values=True)
 
            cod_atividade= from_data.get('codigo-atividade', [''])[0]
            descricao = from_data.get('descricao', [''])[0]
 
            if cod_atividade.strip()== '' or descricao.strip() == '':
               
                # self.send_response(302)
                # self.send_header('Location', '/cadastro_turma_failed')
                # self.end_headers()
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Os campos não foram preenchidos corretamente, tente novamente.".encode('utf-8'))
 
                mensagem_erro = "Os campos não foram preenchidos corretamente, tente novamente!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
 
               
 
           
            elif self.atividade_existente( descricao) == True:
                # self.send_response(302)  
                # self.send_header("Location", "/cadastro_turma_failed")
                # self.end_headers
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Atividade já cadastrada, tente novamente com outros dados.".encode('utf-8'))
                mensagem_erro = "Atividade já cadastrada, tente novamente com outros dados."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
           
            else:
                # Se os campos estiverem preenchidos, adiciona a turma
                self.adicionar_atividade(descricao)
 
                # self.send_response(302)
                # self.send_header("Location", "/cadastrar_atividade")
                # self.end_headers()
 
               
                mensagem_erro = "Atividade cadastrada com sucesso!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
 
                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()
 
                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')
 
                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
 
        else:
            #Se não for a rota definifa, conrinua com o comportamento padrão
            super(MyHandler, self).do_POST()
 
endereco_ip = "0.0.0.0"
porta = 8000
 
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()
 
 