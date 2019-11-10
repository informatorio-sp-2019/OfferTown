
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_OfferTown.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from app_ofertas.models import *

def main():
	try:
			
		r = open('rubros','r')
		rubros = r.readlines()			
		rubros.sort()	
		for rubro in rubros:			
			oRubro = Rubro()
			oRubro.nombre = rubro		
			oRubro.imagen = 'fotos_rubros/'+rubro.strip()+'.svg'
			oRubro.save()

		r.close()		


		l = open ('localidades','r')
		localidades = l.readlines()		
		localidades.sort()
		for localidad in localidades:
			oLocalidad = Localidad()
			oLocalidad.nombre = localidad
			oLocalidad.save()

		l.close()

		p = open ('pagos','r')
		pagos = p.readlines()	
		pagos.sort()	
		for pago in pagos:
			oPago = MedioDePago()
			oPago.nombre = pago
			oPago.save()

		p.close()

	except Exception as e:
		raise e
		print('\n¡¡¡ALGO SALIÓ MAL!!!')
		print(e)
	else:
		print('\n FIN DE LA CARGA!' ) 	


if __name__=='__main__':
	main()


