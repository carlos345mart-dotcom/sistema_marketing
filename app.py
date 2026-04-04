from flask import Flask, render_template
from routes.campanas import campanas_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(campanas_bp)

@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)