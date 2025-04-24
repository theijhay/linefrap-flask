from app import create_app

"""The main entry point for the application"""
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)