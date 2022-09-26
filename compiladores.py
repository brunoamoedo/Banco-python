import sqlite3
import os

con = sqlite3.connect("clientes.db")
cur = con.cursor()
#CRIAR A TABELA CLIENTES

# cur.execute("""CREATE TABLE CLIENTES(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nome TEXT NOT NULL, 
#     data_nascimento TEXT,
#     cpf char(11),
#     estado_civil text not null,
#     nome_mae text

# ) """)




menu = """
CADASTRO DE POTENCIAIS CLIENTES DO PLANO DE SAÚDE
[1]Inserir novos clientes 
[2]Mostrar clientes cadastrados
[3]Gerar txt dos clientes registrados
[4]Fechar o programa
"""
count = 1
while True:
    pgt = input(menu)
    if pgt == '1':
        try:
            cadastro="""
            CADASTRO CLIENTE
            INFORME:
            nome,data de nascimento,cpf,estado civil, nome da mae nessa sequencia e separado por virgula 
            Exemplo:
            bruno valentin dos santos amoedo,09/12/1999,03156176589,solteiro,angelica dos santos ribeiro
               
            """
            pgt = input(cadastro)
            lista = list(pgt.split(','))
            data=[
                (lista[0],lista[1],lista[2],lista[3],lista[4])
            ]
            cur.executemany("""
            INSERT INTO CLIENTES(nome,data_nascimento,cpf,estado_civil,nome_mae)
            values(?,?,?,?,?)
            """,data)
            con.commit()
        except:
            print("Dados invalidos por favor efetue novamente")
    elif pgt == '2':
        res = cur.execute("SELECT * FROM clientes")
        for i in res.fetchall():
            for i,f in enumerate(i):
                if i == 0:
                    print(f"\n{f} - ")
                elif i==1:
                    print(f"Nome: {f}\n")
                elif i==2:
                    print(f"Data nascimento: {f}\n")
                elif i==3:
                    print(f"Cpf: {f}\n")
                elif i==4:
                    print(f"Estado civil: {f}\n")
                elif i==5:
                    print(f"Nome da mãe: {f}\n")
    elif pgt == '3':
        if os.path.isfile('./relatorio.txt'):
            os.remove('./relatorio.txt')
        res = cur.execute("SELECT * FROM clientes")
        for i in res.fetchall():
            for i,f in enumerate(i):
                arquivo = open('relatorio.txt','a')
                if i == 0:
                    arquivo.write(f"\n{f} - ")
                elif i==1:
                    
                    arquivo.write(f"Nome: {f}\n")
                elif i==2:
                    
                    arquivo.write(f"Data nascimento: {f}\n")
                elif i==3:
                    arquivo.write(f"Cpf: {f}\n")
                    
                elif i==4:
                    arquivo.write(f"Estado civil: {f}\n")
                elif i==5:
                    arquivo.write(f"Nome da mae: {f}\n")
        arquivo.close()
        print("Arquivo gerado com sucesso!")          
    elif pgt=='4':
        print("Finalizando o programa")
        break