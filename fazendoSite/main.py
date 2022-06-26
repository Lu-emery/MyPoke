from website import criar_app
import mypokeAPI

def main():
    app = criar_app()
    app.run(debug=True)


if __name__ == "__main__":
    mypokeAPI.deletar_base_de_dados()
    mypokeAPI.criar_base_de_dados()
    mypokeAPI.popularBD()
    main()