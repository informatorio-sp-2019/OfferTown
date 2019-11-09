#!/usr/bin/python3
import os
import csv
import time
import unidecode
from datetime import datetime

# Drive
import io
import json
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from app_ofertas.models import *

def get_api():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

DRIVE = get_api()

def get_file(file):
    meta = DRIVE.files().get(fileId=file, fields='name').execute()
    name = meta['name']
    request = DRIVE.files().get_media(fileId=file)
    filename = os.path.join('fotos_locales', name)
    fh = open(os.path.join('media', filename), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.close()
    return filename

def get_hour(hour_list):
    hour = [datetime.strptime(j, "%H:%M:%S") for j in hour_list]
    return hour

def get_nick(name, lastname):
    nickname = unidecode.unidecode(''.join(e for e in name+lastname if e.isalnum()).lower())
    return nickname

def popular_medio_de_pago():
    medios = ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito"]
    instances_medios = []
    for i in medios:
        medio = MedioDePago(nombre=i)
        medio.save()
        instances_medios.append(medio)
    return instances_medios[0]

def popular_localidades():
    localidades = ["Presidencia Roque Sáenz Peña", "Quitilipi", "Machagai"]
    item_locali = []
    for i in localidades:
        localidad = Localidad(nombre=i)
        localidad.save()
        item_locali.append(localidad)
    return item_locali

def popular_horarios(dia, horas, local):
    horario = Horario(local = local,
                      dia = dia)
    if len(horas) != 0:
        horario.hora_d1 = horas[0].strftime("%H:%M")
        horario.hora_h1 = horas[1].strftime("%H:%M")
        if len(horas) > 2:
            horario.hora_d2 = horas[2].strftime("%H:%M")
            horario.hora_h2 = horas[3].strftime("%H:%M")
    horario.save()

def popular_locales(user, localidades, user_instance, medio):
    local = Local(nombre = user['local'],
                  direccion = user['direccion'],
                  delivery = user['delivery'])
    if user['ciudad'] == 'Presidencia Roque Sáenz Peña':
        local.localidad = localidades[0]
    elif user['ciudad'] == 'Quitilipi':
        local.localidad = localidades[1]
    else:
        local.localidad = localidades[2]
    if user['atencion'] == '24hs':
        local.horario = '24hs'
    else:
        local.horario = 'sh'
    if user['telefono'] != '':
        local.telefono = int(user['telefono'])
    if user['foto'] != '':
        nombre_archivo = get_file(get_foto_id(user['foto']))
        local.imagen = nombre_archivo
    local.usuario = user_instance
    local.save()
    local.metodo_pago.set([medio])
    for i in user['dias']:
        popular_horarios(i, user['horario'], local)

def popular_usuarios(user_list):
    localidades = popular_localidades()
    medio = popular_medio_de_pago()
    nicks = {}
    for user in user_list:
        nick = get_nick(user['nombre'], user['apellido'])
        if nick not in nicks.keys():
            usuario = Usuario(username=nick,
                              first_name = user['nombre'],
                              last_name = user['apellido'],
                              email = nick+'@offertown.com',
                              is_superuser = False,
                              tipo_usuario = 'po',
                             )
            usuario.set_password("qwe123")
            usuario.save()
            nicks[nick] = usuario
        else:
            usuario = nicks[nick]
        popular_locales(user, localidades, usuario, medio)

def get_foto_id(link):
    id = link.split("?id=")[1]
    return id

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
            else:
                people['horario'] = []
            values.append(people)
    return values

def main():
    values = read_values('valores.csv')
    popular_usuarios(values)

if __name__ == '__main__':
    main()
