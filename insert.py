# -*- encoding: utf-8 -*-

"""
	ATENCIÓN: 
		1) Eliminar el archivo sqlite y volver a generar en migrate antes de correr 'insert.py'
	
		2) Falta registrar datos en campos 'imagen' de Rubros, Usuarios.

		3) No se registran datos en las siguientes entidades: Publicaciones, Favoritos, Intereses.

"""

#!/usr/bin/python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



from app_ofertas.models import *

if __name__=='__main__':
	try:
		rubro = Rubro()
		rubro.nombre = 'TIENDA DE ROPAS'
		rubro.save()

		rubro2 = Rubro()
		rubro2.nombre = 'AUTOSERVICIOS'
		rubro2.save()

		rubro3 = Rubro()
		rubro3.nombre = 'RESTAURANTES'
		rubro3.save()

		mdp = MedioDePago()
		mdp.nombre = 'EFECTIVO'
		mdp.save()

		mdp2 = MedioDePago()
		mdp2.nombre = 'TARJ. CRÉDITO'
		mdp2.save()

		mdp3 = MedioDePago()
		mdp3.nombre = 'TARJ. DÉBITO'
		mdp3.save()
					

		lo = Localidad()
		lo.nombre = 'SAENZ PEÑA'
		lo.save()

		lo2 = Localidad()
		lo2.nombre = 'QUITILIPI'
		lo2.save()

		lo3 = Localidad()
		lo3.nombre = 'CHARATA'
		lo3.save()

		u = Usuario()
		u.username = 'ailin89'
		u.lastname = 'CABADAS'
		u.firstname = 'AILIN'
		u.email = 'alin@gmail.com'
		u.password = 'alin123'
		u.set_password(u.password)
		u.tipo_usuario = 'of'
		u.save()


		l = Local()
		l.nombre    = 'HOREB 24HS'
		l.direccion = 'Calle 28 e/ 27 y 29 (Frente al Hospital)'
		l.horario   = '24hs'
		l.usuario   = u
		l.localidad = lo
		l.delivery  = True
		l.telefono  = "3644321221"
		l.save()

		s = Sucursal()
		s.direccion = 'Calle 12 esq 15 (Centro)'
		s.local     = l
		s.localidad = lo
		s.save()

		s2 = Sucursal()
		s2.direccion = 'Calle 10 esq 17 (Centro)'
		s2.local     = l
		s2.localidad = lo
		s2.save()

		s3 = Sucursal()
		s3.direccion = 'Calle 28 y Av. Carlos Gardel (Ensanche Sur)'
		s3.local     = l
		s3.localidad = lo
		s3.save()

		s4 = Sucursal()
		s4.direccion = 'Quitilipi'
		s4.local     = l
		s4.localidad = lo2
		s4.save()

		l2 = Local()
		l2.nombre    = 'BLESS'
		l2.direccion = 'Calle 15 esq 12 (Centro)'
		l2.horario   = '24hs'
		l2.usuario   = u
		l2.localidad = lo
		l2.delivery  = True
		l2.telefono  = "3644321555"
		l2.save()

		s4 = Sucursal()
		s4.direccion = 'Charata'
		s4.local     = l2
		s4.localidad = lo3
		s4.save()

		# **************************************
		# **************************************

		u2 = Usuario()
		u2.username = 'marce89'
		u2.lastname = 'ESCALANTE'
		u2.firstname = 'MARCELINA'
		u2.email = 'marce@gmail.com'
		u2.password = 'marce123'
		u2.set_password(u.password)
		u2.tipo_usuario = 'of'
		u2.save()

		l3 = Local()
		l3.nombre    = 'MARCELA 24HS'
		l3.direccion = 'Calle 51 e/ 18 y 20 (B° Mariano Moreno)'
		l3.horario   = '24hs'
		l3.usuario   = u2
		l3.localidad = lo
		l3.telefono  = "3644221221"
		l3.save()

		s5 = Sucursal()
		s5.direccion = 'Av 33 y Av 2'
		s5.local     = l3
		s5.localidad = lo
		s5.save()

		s6 = Sucursal()
		s6.direccion = 'Calle 9'
		s6.local     = l3
		s6.localidad = lo
		s6.save()

		# HORARIOS
		h = Horario()
		h.local = l2
		h.dia = 'Jueves'
		h.hora_d1 = '21:00'
		h.hora_h1 = '02:00'
		h.save()

		h1 = Horario()
		h1.local = l2
		h1.dia = 'Viernes'
		h1.hora_d1 = '21:00'
		h1.hora_h1 = '02:00'
		h1.save()

		h2 = Horario()
		h2.local = l2
		h2.dia = 'Sabado'
		h2.hora_d1 = '21:00'
		h2.hora_h1 = '03:00'
		h2.save()

		h3 = Horario()
		h3.local = l2
		h3.dia = 'Domingo'
		h3.hora_d1 = '21:00'
		h3.hora_h1 = '03:00'
		h3.save()

		lmdp = LocalMedioDePago()
		lmdp.local = l
		lmdp.medio_de_pago = mdp
		lmdp.save()

		lmdp = LocalMedioDePago()
		lmdp.local = l
		lmdp.medio_de_pago = mdp2
		lmdp.save()

		lmdp = LocalMedioDePago()
		lmdp.local = l
		lmdp.medio_de_pago = mdp3
		lmdp.save()

		lmdp1 = LocalMedioDePago()
		lmdp1.local = l2
		lmdp1.medio_de_pago = mdp
		lmdp1.save()

		lmdp1 = LocalMedioDePago()
		lmdp1.local = l2
		lmdp1.medio_de_pago = mdp2
		lmdp1.save()

		lmdp1 = LocalMedioDePago()
		lmdp1.local = l2
		lmdp1.medio_de_pago = mdp3
		lmdp1.save()


		lmdp2 = LocalMedioDePago()
		lmdp2.local = l3
		lmdp2.medio_de_pago = mdp
		lmdp2.save()

		lmdp2 = LocalMedioDePago()
		lmdp2.local = l3
		lmdp2.medio_de_pago = mdp2
		lmdp2.save()

	except Exception as e:
		raise e
		print('\n¡¡¡ALGO SALIÓ MAL!!!')
		print(e)
	else:
		print('\n FIN DE LA CARGA, PERRO!' ) 	






