#!/usr/bin/python3
import os
import csv
import unidecode
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from app_ofertas.models import *

QUANTITY = 250

def get_hour(hour_list):
    hour = [datetime.strptime(j, "%H:%M:%S") for j in hour_list]
    return hour

def get_nick(name, lastname):
    nickname = unidecode.unidecode(''.join(e for e in name+lastname if e.isalnum()).lower())
    return nickname

def popular_usuarios(user_list):
    for user in user_list:
        nick = get_nick(user['nombre'], user['apellido'])
        usuario = Usuario(username=nick,
                          first_name = user['nombre'],
                          last_name = user['apellido'],
                          email = nick+'@offertown.com',
                          is_superuser = False)
        usuario.set_password("qwe123")
        usuario.save()

def read_values(filename):
    values = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        lista = [row for row in reader]
        lista.remove(lista[0])
        for i in lista:
            people = {"ciudad": i[1],
                   "local": i[2],
                   "direccion": i[3],
                   "telefono": i[4],
                   "delivery": True if i[5] == "Sí" else False,
                   "atencion": i[6],
                   "dias": [j for j in i[13].split(', ')],
                   "foto": i[14],
                   "nombre": i[15],
                   "apellido": i[16]}
            if people['atencion'] == 'Horario Corrido':
                people['horario'] = get_hour(i[7:9])
            elif people['atencion'] == 'Mañana y Tarde':
                people['horario'] = get_hour(i[9:13])
            values.append(people)
    return values

def main():
    values = read_values('valores.csv')
    popular_usuarios(values)

if __name__ == '__main__':
    main()
