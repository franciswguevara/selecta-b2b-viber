from application import init_app

app = create_app()

if __name__ == '__main__':
    app.run(threaded=True, debug = True)