from website import criar_app, deletar_base_de_dados, criar_base_de_dados, popular_bd


def main():
    deletar_base_de_dados()
    criar_base_de_dados()
    popular_bd()
    
    app = criar_app()
    app.run(debug=True)


if __name__ == "__main__":
    
    main()