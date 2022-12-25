
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User

from rest_framework.response import Response

from .serializer import UserSerializer,VerifyAccountSerializer
from .emails import send_otp_via_email

# Create your views here.

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status':200,
                    'message' : 'registration successfully check email',

                    'data':serializer.data,
                })
            return Response({
                'status': 400,
                'message' : 'something went wrong',
                'data' : serializer.errors
            })
           
        except Exception as e:
            print(e)

            

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email = email)
                if not user.exists():
                    return Response({
                    'status': 400,
                    'message' : 'somthing went wrong',
                    'data': 'invalid email'
                })

                if user[0].otp != otp:
                    return Response({
                    'status' : 400,
                    'message' : 'somthing is wrong',
                    'data' : 'wrong otp'
                })

                user = user.first()
                user.is_verified = True
                user.save()





                return Response({
                    'status' : 400,
                    'message': 'account verified',
                    'data' : {},
                })
            return Response({
                'status' : 400,
                'message' : 'somthig went wrong',
                'data' : serializer.errors
            })

        except Exception as e:
            print(e)


            
