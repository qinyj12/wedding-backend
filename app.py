from factory import creat_app

app = creat_app()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host = "0.0.0.0", port = 5000)