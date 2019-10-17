#!/usr/bin/python3
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from app_ofertas.models import *

QUANTITY = 250

def generate_users():
    nombre = ['Jorge', 'Carlos', 'Joaquín', 'Marcelo', 'Fabián', 'Fabiola',
            'Carlita', 'Mario', 'Mariano', 'Mariana', 'María', 'Jorgelina', 'Ernesto',
            'Ernestina', 'Delfina', 'Luciano', 'Luciana', 'Isidro', 'Vladimir', 'Dimitri',
            'Yuri', 'Simón', 'Norberto', 'Alberto', 'Agustín', 'Juan', 'Matías', 'Ricardo',
            'Guido', 'Alfonso', 'Nicolás', 'Francisco', 'Fernando', 'Fernanda', 'Pablo',
            'Leonardo', 'Rogelio', 'Roberto', 'Luis', 'Miguel', 'Angel', 'Romero', 'Giorgio',
            'Rafael', 'Manuel', 'Adolfo', 'Rodolfo', 'Levy', 'Ulises', 'Emanuel']
    apellidos = ['Harasiwka', 'Martínez', 'Adami', 'Polich', 'Godo', 'Storani', 'Cejas',
                'Dupraz', 'Gómez', 'Sánchez', 'Juarez', 'Roca', 'Videla', 'Bielsa',
                'Gallardo', 'Fernández', 'Riquelme', 'Román', 'Messi',
                'López', 'Ibalo', 'Mollo', 'Arnedo', 'Echeverría', 'Márquez', 'Gagarin',
                'Prieto', 'Aguas', 'Planta', 'Spinetta', 'Armani', 'Andrada', 'Donatello',
                'Moroder', 'Bangalter', 'Estrada', 'Laprida', 'Belgrano', 'Báez',
                'Páez', 'Wozniak', 'Mores', 'Mandela', 'Dybala', 'Napolitano', 'Jiménez',
                'Gil', 'Vázquez', 'Ramírez']
    results = []
    for i in range(0, QUANTITY):
        fn = random.choice(nombre)
        ln = random.choice(apellidos)
        nick = generate_nickname(fn, ln)
        user = {'Nombre': fn,
            'Apellido': ln,
            'Nickname': nick,
            'Mail': nick.lower()+'@gmail.com', # Lower again in case of the easter egg being triggered
            'Tipo': random.choice(['Oferente', 'Ofernauta'])}
        results.append(user)
    return results

def generate_nickname(nombre, apellido):
    nick = nombre+apellido + str(random.randint(243, 6383))
    nick = nick.lower()
    return nick

def generate_places():
    prefijo = ['San', 'Villa']
    base = ['Los Pollos', 'La Lucha', 'Don Jorge', 'Las Toninas', 'Altos Zanjones', 'Bellos Paseos',
            'Grandes Rocas', 'Diversas Rutas', 'Los Caminos', 'Las Aves', 'Miradas', 'Caricias Significativas',
            'Las Verdades']
    sufijo = ['Andes', 'Pastos', 'Peces Multicolores', 'Terrenos', 'Cantos Bonitos', 'Arboles', 'Recuerdos',
            'Tesoros', 'Campos']
    resultados = []
    for i in base:
        if random.choice([True,False]):
            nombre = random.choice(prefijo) + ' ' + i
        else:
            nombre = i
        if random.choice([True, False]):
            nombre = nombre + ' de los ' + random.choice(sufijo)
        resultados.append(nombre)
    return resultados

def generate_streets():
    calles = ['Avellaneda', 'Láprida', 'Belgrano', 'San Martín', 'Asunción', '1era Junta', 'Obligado', 'Las Heras',
            '27 de Febrero', '9 de Julio', 'Achával Rodríguez', 'Acoyte', 'Albarellos', 'Alberdi', 'Leandro Alem',
            'Almafuerte', 'Álvarez Jonte', 'Alvear', 'Alcorta', 'Antártida Argentina', 'Aranguren', 'Asamblea',
            'Asturias', 'Boedo', 'Boyacá', 'Cabildo', 'Calabria', 'Callao', 'Caseros', 'Congreso', 'Córdoba', 'Coronel Roca',
            'Corrientes', 'Crámer', 'Larralde', 'Dorrego', 'Escalada', 'Eva Perón', 'Figueroa Alcorta', 'Gaona', 'García del Río',
            'Garay', 'Independencia', 'Juramento', 'La Plata', 'Lacarra', 'Lope de Vega', 'Madero', 'Medrano', 'Nazca',
            'Colón', 'Pueyrredón', 'Rivadavia', 'Sarmiento', 'Segurola', 'Udaondo', 'Triunvirato', 'Uruguay', 'Velez Sarsfield',
            'Warnes', 'Agüero', 'Arroyo', 'Balcarce', 'Bolívar', 'Butteler', 'Castillo', 'Concordia', 'Cervantes', 'Cespedes',
            'Defensa', 'Florida', 'Galván', 'Iberá' 'Jacarandá', 'Ituzaingo', 'Junín', 'Lanín', 'Lavalle', 'Libertad',
            'Luna', 'Mataco', 'Medrano', 'Mitre', 'Natal', 'Newbery', 'Niza', 'Nogoya', 'Núñez', 'Ñandutí', 'Orma',
            'Reconquista', 'Tacuara', 'Urquiza', 'Valdenegro', 'Valle', 'Varela', 'Velázquez', 'Voltaire', 'Yapeyú',
            'Yrupé', 'Zapala', 'Caminito']
    resultado = random.choice(calles) + ' ' + str(random.randint(1, 1500))
    return resultado

def generate_rubros(localidades):
    rubros = {'Ferretería': ('El Tornillo', 'La Victoria', 'El Rancho', 'Él Óxido', 'Los de Hierro'),
            'Panadería': ('Buen Pan', 'La Roma', 'La Delicia', 'San Jorge', 'La Harina', 'La Providencia'),
            'Artículos de Computación': ('Super-Byte', 'Cluster', 'El Circuito', 'Neo-Tech', 'IronMountain', 'Star War'),
            'Deportes y Fitness': ('El Fisicudo', 'Los Campeones', 'Salud', 'Buen Cuerpo'),
            'Electrodomésticos': ('Hogareño', 'Datan', 'Megatech', 'Electromundo', 'FullTrace'),
            'Construcciones': ('SuperHouse', 'Power Brick', 'Ultra-Build', 'Argen-Casas'),
            'Librería': ('El Libro', 'La Lectura', 'Kafkianos', 'Montecristo', 'Lo de Pocho'),
            'Tienda de Música': ('Disco-Max', 'Como Cusack', 'El Radial', 'Estelares', 'Fantasticia'),
            'Celulares': ('MobilePro', 'Dr Celular', 'Movitel', 'SmartWay', 'El Teléfono'),
            'Rotisería': ('El Parrillazo', 'Alta Paty', 'Carnes Argentas', 'El Encuentro', 'Buen Domingo'), 
            'Cotillón': ('El Fiestero', 'Diversiones', 'Festejoso', 'Coloridos Colores')}
    negocios = list()
    for i in rubros.keys():
        for j in rubros[i]:
            negocio = {'Nombre': i+' '+j,
            'Rubro': i,
            'Localidad': random.choice(localidades),
            'Direccion': generate_streets()}
            if random.choice((True, False)):
                negocio['Sucursales'] = [generate_streets() for k in range(0, random.randrange(1,3))]
            negocios.append(negocio)
    return negocios
                
def popular_usuarios(user_list):
    for user in user_list:
        db_user = User(username=user['Nickname'], is_superuser=0, first_name=user['Nombre'],
                last_name=user['Apellido'], email=user['Mail'])
        print(db_user, user['Mail'])
        db_user.save()


def main():
    # Oferente
    # Ofernauta 
    usuarios = generate_users()
    #localidades = generate_places()
    #rubros = generate_rubros(localidades)
    popular_usuarios(usuarios)

if __name__ == '__main__':
    main()
