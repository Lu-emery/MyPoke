from website import inicializar_mypoke, criar_app


def main():
    inicializar_mypoke()
    
    app = criar_app()
    app.run()


if __name__ == "__main__":
    
    main()