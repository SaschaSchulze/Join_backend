from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import path

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=email, email=email, password=password)
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all().values('id', 'username', 'email')
    return JsonResponse({'users': list(users)})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def set_item(request):
    key = request.data.get('key')
    value = request.data.get('value')

    request.session[key] = value
    return Response({'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_item(request):
    key = request.GET.get('key')
    if not key:
        return Response({'error': 'Key is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if key == 'users':
        users = User.objects.all().values('id', 'username', 'email')
        return Response({'data': {'value': list(users)}})
    
    return Response({'error': 'Invalid key'}, status=status.HTTP_400_BAD_REQUEST)