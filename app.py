from library_management_system import start_app

app, db = start_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
