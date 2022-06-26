from website import inicializar_mypoke


def main():
    inicializar_mypoke()
    
    app = criar_app()
    app.run(debug=True)


if __name__ == "__main__":
    
    main()