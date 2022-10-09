import sqlite3
con = sqlite3.connect("clientes.db")
cur = con.cursor()

#CRIAR A TABELA CLIENTES Só execute uma unica vez depois comente ou apague!
# cur.execute("""CREATE TABLE CLIENTES(
#     id INTEGER PRIMARY KEY AUTOINCREMENT, 
#     nome TEXT,
#     cpf text, 
#     saldo float) """)

menu = '''
[B] Buscar conta
[C] Cadastrar a conta
[D] Deposito    
[E] Extrato
[S] Saque
Para finalizar digite "SAIR"
'''
LIMITE_SAQUE = 3
MAX_DEPOSITO = 500
saldo = 0

while True:
    pgt=input(menu)
    if pgt.upper() == "B":
        codigo_cpf = input("informe seu cpf: ")
        res = cur.execute(f"SELECT id,nome FROM clientes where cpf = {codigo_cpf}")
        if res != []:
            for i in  res.fetchall():
                    print(f"{i[1]}, O seu codigo para deposito é: {i[0]} use para depositar na sua conta!") 
        else:
            print("Cpf não cadastrado")
            pgt = "B"
    if pgt.upper() == "C":
        nome=input("Informe seu nome: ")
        cpf = input("Informe seu cpf sem pontuações: ").strip()
        cpf.replace('.','').replace(',','')
        if len(cpf) != 11:
            pgt = "C"
            print("Cpf invalído informe o novamente!")
        else:
            cur.execute(f"INSERT INTO CLIENTES(nome,cpf) values('{nome.upper()}','{cpf}')")
            con.commit()
            res = cur.execute(f"select id from clientes where cpf = {cpf}")
            for i in  res.fetchall():
                print(f"O seu codigo para deposito é: {i[0]} use para depositar na sua conta!")    
    if pgt.upper() == "D":
        codigo=int(input("informe o codigo para deposito: "))
        res = cur.execute(f"SELECT * FROM clientes where id = {codigo}")
        if res.fetchall() != []:
            valor=(input("informe o valor: ").replace(',','.'))
            if  valor.isdigit():
                saldo1 = cur.execute(f"select saldo from clientes where id = {codigo}")
                saldo1 = saldo1.fetchall()
                saldo1 = 0 if saldo1[0][0] is None else saldo1[0][0]
                saldo_final= float(saldo1) + float(valor)
                cur.execute(f"UPDATE CLIENTES SET saldo = {saldo_final} where id={codigo}")
                con.commit()
            else:
                print("valor invalido")
                pgt = "E"
        else:
            print("Informe o codigo novamente, codigo invalido")
            pgt = "E"
    elif pgt.upper()=="E":
        codigo = input("Informe o seu codigo: ")
        res = cur.execute(f"SELECT nome,saldo FROM clientes where id = {codigo}")
        if res != []:
            for i in res.fetchall():
                if i[1] == None:
                    saldo_aux = 0
                else:
                    saldo_aux = i[1]
                print(f"{i[0]} o seu saldo é: R$ {saldo_aux:.2f}")
        else:
            print("codigo não encontrado")
            pgt = "E"
    elif pgt.upper()=="S":
        codigo=int(input("informe o codigo para deposito: "))
        saque = float(input("informe o valor que deve ser sacado: "))
        res = cur.execute(f"SELECT saldo FROM clientes where id = {codigo}")
        res = res.fetchall()
        if not res == []:
            saldo = 0 if res[0][0] is None else res[0][0]
            if saque <= 500 and saque <=saldo and LIMITE_SAQUE != 0:
                saldo-=saque
                print(f"Operação realizado com sucesso! saldo atual: R${saldo:.2f} ")
                cur.execute(f"UPDATE CLIENTES SET saldo = {saldo} where id = {codigo}")
                con.commit()
                LIMITE_SAQUE-=1
            elif LIMITE_SAQUE == 0:
                print("LIMITE DE SAQUE ATINGIDO")
            elif saque > saldo:
                print("Você não possui saldo suficiente!")
            elif saque > 500:
                print("Saque invalido o saque tem um limite de 500,00 reais!")
        else:
            print("codigo não encontrado")
            pgt = "E"
    elif pgt.upper() == 'SAIR':
        print("Finalizando o programa!")
        break