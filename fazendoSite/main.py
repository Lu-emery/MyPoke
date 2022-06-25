from website import criar_app


def main():
    app = criar_app()

    app.run(debug=True)


if __name__ == "__main__":
    main()