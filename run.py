from fundsapp import create_app

starter = create_app()

if __name__ == "__main__":
    starter.run(debug = True, port = 8700)
    