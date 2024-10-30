from myapp import create_app
from flask import redirect, url_for

app = create_app()

# Checking template folder path
print("Template folder paths:", app.template_folder)

@app.route('/')
def root():
    return redirect(url_for('main.login'))

if __name__ == '__main__':
    app.run(debug=True)