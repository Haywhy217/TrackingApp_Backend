from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from utils.utils import create_jwt_token
from django.contrib.auth import logout as auth_logout
import json


User = get_user_model()


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            data_dict = json.loads(json_data)
        
            email = data_dict.get("email")
            username = data_dict.get("username")
            password = data_dict.get("password")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "User already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already in use"}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            return JsonResponse({"message": "Registration Successful"}, status=201)
        
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid method. Use POST."}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            data_dict = json.loads(json_data)

            username = data_dict.get("username")
            password = data_dict.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                token = create_jwt_token(user)
                response = JsonResponse({"message": "Login successful", "token": token})
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response

            return JsonResponse({"message": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    return JsonResponse({"message": "Invalid method. Use POST."}, status=405)

@csrf_exempt
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"message": "Invalid method. Use POST."}, status=405)
