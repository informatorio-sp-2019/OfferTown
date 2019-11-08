#!/usr/bin/python3
import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

#from app_ofertas.models import *

QUANTITY = 250

def popular_usuarios(user_list):
    for user in user_list:
        db_user = User(username=user['Nickname'], is_superuser=0, first_name=user['Nombre'],
                last_name=user['Apellido'], email=user['Mail'])
        print(db_user, user['Mail'])
        db_user.save()


def main():
    #usuarios = generate_users()
    #localidades = generate_places()
    #rubros = generate_rubros(localidades)
    #popular_usuarios(usuarios)
    #popular_rubros()
    values = sheets.get_values()
    print(values)
    """
    people = [{"ciudad": i[0],
               "local": i[1],
               "direccion": i[2],
               "delivery": True if i[3] == "Sí" else False,
               "atencion": i[4],
               "telefono": i[5],
               "dias": [j for j in i[6].split(', ')],
               "nombre": i[9],
               "apellido": i[10],
               "foto": i[11],
               "horario": (get_time_range(i[13], i[14], i[4]),
                           get_time_range(i[15], i[16], i[4]))
               } for i in values]
    print(people)
    """

if __name__ == '__main__':
    main()
