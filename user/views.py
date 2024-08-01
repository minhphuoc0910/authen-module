from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.utils import timezone

# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if request.COOKIES.get('jwt'):
            raise AuthenticationFailed('Already logged in!')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User does not exist')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=600),
            'iat': timezone.now()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response({
            'jwt': token
        })
        response.set_cookie(key='jwt', value=token, httponly=True)
        user.last_login = timezone.now()
        user.save()  
        return response
    
class UserProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        print(payload)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserLogoutView(APIView):
    def post(self, request):
        if not request.COOKIES.get('jwt'):
            raise AuthenticationFailed('Unauthenticated!')
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'Logged out'
        }
        return response