from django.contrib.auth.models import User
from portal.models import Usuario,Us
import md5
 
class RedtelBackend(object): 
    """ 
    Autentificacion contra la configuracion de usuarios del sistema 
    redtel.
    """ 
    def authenticate(self, username=None, password=None): 
        'metodo que realizara la autentificacion contra la tabla usuarios' 
        'de redtel.'
        usuario = Us.objects.get(username=username)
        encript = md5.new(password).hexdigest()
        if encript == usuario.password: 
            try: 
               user = User.objects.get(username=username) 
            except User.DoesNotExist: 
                # Crea un nuevo usuario. Nota que podemos fijar un password 
                # para cualquiera, porque este no sera comprobado; el password 
                # de settings.py lo hara. 
                rut = usuario.rut
                n=len(rut)
                if n==12 :
                    rut = '0'+rut.upper()
                else:
                    rut = '00'+rut.upper()
                user = User(username=username, password=usuario.password,first_name=rut)
                user.save() 
            return user 
        return None 
 
    def get_user(self, user_id): 
        try: 
           return User.objects.get(pk=user_id) 
        except User.DoesNotExist: 
            return None

 
    def get_user(self, user_id): 
        try: 
           return User.objects.get(pk=user_id) 
        except User.DoesNotExist: 
            return None
