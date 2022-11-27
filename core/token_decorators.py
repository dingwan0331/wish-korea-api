import jwt

from django.http  import JsonResponse

from auth.models       import User
from wish_korea.settings import SECRET_KEY , ALGORITHM

def verify_token(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get("Authorization",None)
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user = User.objects.get(id=payload['user_id'])
            request.user = user  
            
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message' : 'Expire Access Token'}, status = 401)
            
    return wrapper