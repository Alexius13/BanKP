from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import folium
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Creando los modelos para la base de datos
class EntidadFinanciera (db.Model):#herencia
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    pagina = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(10000), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, categoria, pagina, contacto, imagen, lat, lon):
        self.nombre = nombre
        self.categoria = categoria
        self.pagina = pagina
        self.contacto = contacto
        self.imagen = imagen
        self.lat = lat
        self.lon = lon


@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/aprende')
def aprende():
    return render_template('aprende.html')

@app.route('/crece', methods = ['GET','POST'])
def crece():
    ubicaciones = EntidadFinanciera.query.all()
    filtro_cat=''
    # limpiando categorias para pasar al front para una selección
    resultados = []
    for ubicacion in ubicaciones:
        resultados.append(ubicacion.categoria)

    categorias = []
    for resultado in resultados:
        if resultado not in categorias:
            categorias.append(resultado)

    if request.method == 'POST':
        
        filtro_cat = request.form['categoria']
        
    return render_template('crece.html', categorias=categorias, filtro=filtro_cat)       

@app.route('/informate')
def informate():
    return render_template('informate.html')

@app.route('/test')
def test():
    return render_template('test.html')      

@app.route('/mapa/',defaults={'filtro': 'Banco'})
@app.route('/mapa/<filtro>')
def mapa(filtro):
    #print(f'Mapa: {entidad_por_categoria[0].categoria}')
    coordenadas_inicio = [-25.30234132846098, -57.58115713076387] 
    mapa = folium.Map(location=coordenadas_inicio, zoom_start=20) # creamos el mapa pasandole las coordenadas y el nivel de zoom y guardamos en la variable mapa
    #ubicaciones = EntidadFinanciera.query.all() # obtenemos todas las ubicaciones de la base de datos
    ubicaciones = EntidadFinanciera.query.filter(EntidadFinanciera.categoria == filtro).all()
    if ubicaciones:
        for ubicacion in ubicaciones:
            print(ubicacion.categoria)
            tarjeta = f"""
                <div class="card" style="width: 350px;">
                <img src="{ubicacion.imagen}" class="card-img-top" alt="...">
                <div class="card-body">
                <h4><b class="card-title">{ubicacion.nombre}</b></h4>
                <p class="card-text"><h5><ul></li><li><b>Categoria:</b> {ubicacion.categoria}</li><li><b>
                Contacto: </b>{ubicacion.contacto}</li><li><b>Para crear una cuenta presione: </b></li></p></ul></h5></p>
                <a href="{ubicacion.pagina}" class="btn btn-primary" style="color: #fff; font-size: 18px; font-weigth: bolder;">Ir a la pagina</a>
                </div>
                </div>"""

            folium.Marker([ubicacion.lat, ubicacion.lon], popup=tarjeta, tooltip="Click para mas info",icon=folium.Icon(color='red',icon='credit-card')).add_to(mapa)
    
    return mapa._repr_html_()
@app.route('/agregar-marcadores', methods=['GET', 'POST'])

def agregar_marcadores ():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        pagina = request.form['pagina']
        contacto = request.form['contacto']
        imagen = request.form['imagen']
        lat = request.form['lat']
        lon = request.form['lon']

        entidad_financiera = EntidadFinanciera(nombre=nombre, categoria=categoria, pagina=pagina, contacto=contacto, imagen=imagen,lat=lat, lon=lon)
        db.session.add(entidad_financiera)
        db.session.commit()

        return redirect(url_for('mapa'))
    return render_template('agregar_marcadores.html')        

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all(bind_key='__all__')
    