from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/aprende')
def aprende():
    return render_template('aprende.html')

@app.route('/crece')
def aprende():
    return render_template('crece.html')       

@app.route('/informate')
def aprende():
    return render_template('informate.html')       


if __name__ == '__main__':
    app.run(debug=True)
    