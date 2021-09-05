import random
import secrets

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User, UserData, Winner
from .serializers import UserSerializer, UserDataSerializer, WinnerSerializer
from .validators import check_email
from .emails import send_mail


URL_BASE = settings.URL_BASE


class UserViewSet(ViewSet):
    '''
    Endpoint to register initial user data in a model UserData, generates the token to validate the Email

    @:param username, email, first_name, last_name

    method: POST

    example payload: {"username": wolfracer, "email": email@gmail.com, "first_name": jon, "last_name": doe}

    response: http 200, {'menesaje': 'registro exitoso, revise su correo para validar su email'}

    if not unique email, an error response is raise: {'error': 'ya existe una cuenta con ese email'} http 400
    '''

    serializer_class = UserDataSerializer
    queryset = UserData.objects.all()

    def create(self, request):

        serializer = UserDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = check_email(serializer.validated_data.get('email'))
        token = secrets.token_urlsafe()
        user = UserData.objects.create(token=token, **serializer.validated_data)
        url = f'{URL_BASE}/api/validate/{token}/'
        #anymail se encarga se mandar el correo en segundo plano, la respuesta es inmediata practicamente.
        send_mail(email, url, user.first_name)  # TODO: poner con celery.
        return Response({'menesaje': 'registro exitoso, revise su correo para validar su email'})


class ValidateUserViewSet(ViewSet):

    '''
    Endpoint to validate email, comparing stored token vs the one recieved in the email

    example request: PUT /api/validate/<token>/ payload: {'password': <your password>}

    example success response: http 200, {'mensaje': 'Usuario validado con exito'}

    error response: http 400 {'error': 'El token enviado es incorrecto'}
    '''

    def update(self, request, pk=None):

        token = pk
        user_data = UserData.objects.filter(token=token).first()
        if user_data:
            user = User.objects.create_user(
                password=request.data.get('password'), username=user_data.username, first_name=user_data.first_name,
                last_name=user_data.last_name, email=user_data.email
            )
            return Response({'mensaje': 'Usuario validado con exito'})
        return Response({'error': 'El token enviado es incorrecto'}, status=status.HTTP_400_BAD_REQUEST)


class SelectWinnerViewSet(ViewSet):

    '''
    endpoint to select a random winner among every user

    exammple request: GET /api/winner/

    success response: http 200 {"user": {"username": "wolfracer"... "date":"04/09/2021"}

    error response: http 404 {"error": "No hay usuarios registrados en el sistema"}
    '''

    def list(self, request):

        users_ids = User.objects.all().values('id')
        if users_ids:
            random_id = random.choice(users_ids)["id"]
            user = User.objects.get(pk=random_id)
            winner = Winner.objects.create(user=user)
            serializer = WinnerSerializer(winner)
            return Response(serializer.data)
        return Response({"error": "No hay usuarios registrados en el sistema"})
