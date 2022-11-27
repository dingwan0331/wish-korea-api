import json

import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from auth.models        import User
from order.models       import Cart
from core.token         import Token
from core.validators    import (
    validate_names,
    validate_email,
    validate_password,
    validate_phone_number
)

class SignUpView(View):
    def post(self, requst):
        try:
            data = json.loads(requst.body)
            username     = data['username']
            password     = data['password']
            email        = data['email']
            phone_number = data['phone_number']
            name         = data['name']
            nick_name    = data.get('nick_name','')
            address      = data.get('address','')

            validate_names(username, nick_name, name)
            validate_email(email)
            validate_phone_number(phone_number)
            validate_password(password)        

            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            print(len(hashed_password))

            if User.objects.filter(username = username).exists():
                return JsonResponse({'message' : 'Duplicated username'}, status = 400)        

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'Duplicated email'}, status = 400)

            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message' : 'Duplicated phone number'}, status = 400)

            User.objects.create(
                username     = username,
                password     = hashed_password,
                email        = email,
                phone_number = phone_number,
                name         = name,
                nick_name    = nick_name,
                address      = address
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 401)
        
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

            user     = User.objects.get(username = username)

            if not bcrypt.checkpw(password.encode('utf-8') , user.password):
                return JsonResponse({"message" : "Invalid User"}, status = 401)
            
            access_token  = Token('access_token').sign_token(user.id)
            refresh_token = Token('refresh_token').sign_token(user.id)

            Cart.objects.filter(user_id = user.id).delete()

            response = JsonResponse({'access_token' : access_token}, status = 200)
            response.set_cookie('refresh_token', value=refresh_token, httponly=True,max_age=28800)
            return response

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'Ivalid User'}, status = 401)

class TokenView(View):
    def get(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            access_token  = Token('access_token').resign_token(refresh_token)

            return JsonResponse({'access_token' : access_token}, status = 200)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message' : 'Refresh Token Expire'}, status = 401)