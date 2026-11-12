
import json

ARQUIVO = "alunos.json"


def carregar_alunos():
    """Lê os alunos salvos. Se ainda não houver arquivo, começa vazio."""
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)
        if not isinstance(alunos, list):
            raise ValueError("O arquivo não contém uma lista de alunos.")
        return alunos
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, ValueError, OSError) as erro:
        print(f"Erro ao ler {ARQUIVO}: {erro}")
        return None


def salvar_alunos(alunos):
    """Grava a lista no arquivo JSON."""
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(alunos, arquivo, ensure_ascii=False, indent=4)
        return True
    except OSError as erro:
        print(f"Erro ao salvar os alunos: {erro}")
        return False


def ler_numero(mensagem, minimo=1, maximo=None):
    """Pede um número inteiro e impede valores inválidos."""
    while True:
        try:
            numero = int(input(mensagem))
            if numero < minimo or (maximo is not None and numero > maximo):
                print("Número fora do intervalo permitido. Tente novamente.")
            else:
                return numero
        except ValueError:
            print("Digite um número inteiro válido.")


def buscar_aluno(alunos, codigo):
    for aluno in alunos:
        if aluno["codigo"] == codigo:
            return aluno
    return None


def cadastrar_aluno(alunos):
    print("\n--- CADASTRAR ALUNO ---")
    codigo = ler_numero("Código do aluno: ")

    if buscar_aluno(alunos, codigo) is not None:
        print("Já existe um aluno com esse código!")
        return

    nome = input("Nome: ").strip()
    while not nome:
        print("O nome não pode ficar vazio.")
        nome = input("Nome: ").strip()

    idade = ler_numero("Idade: ", 1, 120)
    novo_aluno = {"codigo": codigo, "nome": nome, "idade": idade}
    alunos.append(novo_aluno)

    if salvar_alunos(alunos):
        print("Aluno cadastrado com sucesso!")
    else:
        alunos.remove(novo_aluno)


def listar_alunos(alunos):
    print("\n--- LISTA DE ALUNOS ---")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for aluno in alunos:
        print(f"Código: {aluno['codigo']} | Nome: {aluno['nome']} | Idade: {aluno['idade']}")


def consultar_aluno(alunos):
    print("\n--- CONSULTAR ALUNO ---")
    codigo = ler_numero("Digite o código do aluno: ")
    aluno = buscar_aluno(alunos, codigo)

    if aluno is None:
        print("Aluno não encontrado.")
    else:
        print(f"Código: {aluno['codigo']}")
        print(f"Nome: {aluno['nome']}")
        print(f"Idade: {aluno['idade']}")


def alterar_aluno(alunos):
    print("\n--- ALTERAR ALUNO ---")
    codigo = ler_numero("Digite o código do aluno: ")
    aluno = buscar_aluno(alunos, codigo)

    if aluno is None:
        print("Aluno não encontrado.")
        return

    print("Deixe em branco para manter a informação atual.")
    nome = input(f"Novo nome ({aluno['nome']}): ").strip()
    idade_texto = input(f"Nova idade ({aluno['idade']}): ").strip()

    if idade_texto:
        try:
            idade = int(idade_texto)
            if not 1 <= idade <= 120:
                print("A idade deve estar entre 1 e 120. Alteração cancelada.")
                return
        except ValueError:
            print("Idade inválida. Alteração cancelada.")
            return
    else:
        idade = aluno["idade"]

    dados_antigos = aluno.copy()
    if nome:
        aluno["nome"] = nome
    aluno["idade"] = idade

    if salvar_alunos(alunos):
        print("Aluno alterado com sucesso!")
    else:
        aluno.update(dados_antigos)


def excluir_aluno(alunos):
    print("\n--- EXCLUIR ALUNO ---")
    codigo = ler_numero("Digite o código do aluno: ")
    aluno = buscar_aluno(alunos, codigo)

    if aluno is None:
        print("Aluno não encontrado.")
        return

    confirmar = input(f"Excluir {aluno['nome']}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Exclusão cancelada.")
        return

    posicao = alunos.index(aluno)
    alunos.remove(aluno)
    if salvar_alunos(alunos):
        print("Aluno excluído com sucesso!")
    else:
        alunos.insert(posicao, aluno)


def main():
    alunos = carregar_alunos()
    if alunos is None:
        print("Não foi possível abrir os dados. O programa será encerrado sem alterar o arquivo.")
        return

    while True:
        print("\n===== CADASTRO DE ALUNOS =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Consultar aluno")
        print("4 - Alterar aluno")
        print("5 - Excluir aluno")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_aluno(alunos)
        elif opcao == "2":
            listar_alunos(alunos)
        elif opcao == "3":
            consultar_aluno(alunos)
        elif opcao == "4":
            alterar_aluno(alunos)
        elif opcao == "5":
            excluir_aluno(alunos)
        elif opcao == "0":
            print("Encerrando o sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
