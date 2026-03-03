from search import search_prompt

def main():
    print("Chat iniciado! Digite 'sair' para encerrar.\n")

    while True:
        # Solicita a pergunta do usuário e remove espaços em branco extras.
        pergunta = input("PERGUNTA: ").strip()

        if pergunta.lower() == "sair":
            print("Encerrando o chat...")
            break

        if not pergunta:
            continue

        # Chama a função de busca para obter a resposta com base na pergunta do usuário. 
        resposta = search_prompt(pergunta)

        print(f"RESPOSTA: {resposta}")
        print("\n---\n")

if __name__ == "__main__":
    main()
