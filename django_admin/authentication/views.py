from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import uuid
from django.shortcuts import redirect
from django.http import JsonResponse
import datetime
from rest_framework import status
from .models import Users
# from django.core.mail import send_mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import RequestContext, loader
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.hashers import make_password

# from django.core.mail import EmailMessage

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        email = request.data['email']
        username = request.data['user_name']
        print('email',email) 
        
        response = Response()
        email_exists = Users.objects.filter(email=email).first()
        username_exists = Users.objects.filter(user_name=username).exists()
        print('username',username_exists)
        if username_exists and email_exists:
            message = {
            'message': 'Username and email already exist'
        }  
            return Response(message, status=status.HTTP_409_CONFLICT)

        elif email_exists  :
            message = {
            'message': 'User email already exist'
        }
            return Response(message, status=status.HTTP_409_CONFLICT)
       
        elif username_exists:
            message = {
            'message': 'User name already exist'
        }
            return Response(message, status=status.HTTP_409_CONFLICT)



            # return response, status.HTTP_409_CONFLICT
        else:
            try:
                token = str(uuid.uuid4())
                context = {'token': token}
             
                template = 'conformation-email-template.html'
            # html_content = render_to_string(template,context,domain= current_site,)
            # html_content = render_to_string(template, {  
            #     'domain': current_site,  
            #     'context':context,
            #     'token':token,  
            # })  
                html_content = loader.get_template(template).render(
                    {'context': context, 'token': token},
                    request=request
                )
            
                text_content = strip_tags(html_content)
                message = EmailMultiAlternatives(
                    subject='Confirm Your Registration',
                    body=text_content,
                    from_email='joybrata007@gmail.com',
                    to=[email]
                )
                message.attach_alternative(html_content, "text/html")
                message.send(fail_silently=False)
                hashed_password = make_password(request.data['password'])
                request.data['password'] = hashed_password  # Update the password field with the hashed password
                serialization = UserSerializer(data=request.data)
                serialization.is_valid(raise_exception=True)
                serialization.save()

                response.data = {
                    'message': 'An email has been sent to your email address with instructions to confirm your registration.',
                    'token': token
                }
            except Exception as e:
                print('-------', e)
                response.data = {
                    'message': 'An error occurred while sending the email. Please try again later.'
                }

        # if user or username_exists is not None:
        #     try:
        #         response.data = {
        #             'message': 'User already signed up'
        #         }
        #     except Exception as e:
        #         print('-------',e)
        #         response.data = {
        #             'message': 'An error occurred while sending the email. Please try again later.'
        #         }
        # else:

        #     response.data = {
        #         'message': 'An email has been sent to your email address with instructions to confirm your registration.',
        #         'token':token
        #     }

        return response


# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = Users.objects.filter(email=email).first()
#         # user.set_password(user.password)
#         print('user', user)
#         if user is None:
#             raise AuthenticationFailed('User not found')
#         print('password',user.check_password(password))
#         if user.check_password(password):
#             payload = {
#                 'id': user.id,
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#                 'iat': datetime.datetime.utcnow()
#             }
#             print(payload)
#             # token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf8')
#             token = jwt.encode(payload, "secret", algorithm="HS256")
#             print(token)
#             response = Response()
#             response.set_cookie(key='jwt', value=token, httponly=True)
#             response.data = {
#                 'message': 'Login successful',
#                 'jwt': token
#             }
#             return response

#         raise AuthenticationFailed('Incorrect password')
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = Users.objects.get(email=email)
            print('user',user)
        except Users.DoesNotExist:
            raise AuthenticationFailed('User not found')

        if user.check_password(password):
            print('inside')
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            print('---=======================---payload',payload)
            token = jwt.encode(payload, "secret", algorithm="HS256")
            print('===================================token',token)
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            print('--------------------',user)

            serializer = UserSerializer(user)
            print('serializer',serializer.data)
            response.data = {
                'message': 'Login successful',
                'jwt': token,
                'user': {
                    'id': user.id,
                    **serializer.data
                }
            }
            return response

        raise AuthenticationFailed('Incorrect password')



class UserView(APIView):
    def get(self, request):
        token = request.COOKIES['jwt']
        print(token)
        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        user = Users.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        print(serializer)
        return Response(serializer.data)


class LogoutView(APIView):
    def delete(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
        }
        return response



class forgotPasswordView(APIView):
    def post(self, request):
        merge_data = {
        'greetings': "hello"
          }
        template = 'matching-jobs.html'
        html_content=render_to_string(template)
        text_content=strip_tags(html_content)
        print(text_content)
        email = request.data['email']
        response = Response()
        user = Users.objects.filter(email=email).first()
        print(user)
        
        serializer = UserSerializer(user)
        if user is not None:
            try:
                

                message = EmailMultiAlternatives(
                subject='Django HTML Email',
                body="mail testing",
                from_email='joybrata007@gmail.com',
                to=[user],
                
                )
                message.attach_alternative(html_content, "text/html")
                message.send(fail_silently=False)
                response.data = {
                    'message': 'An email has been sent to your email address with instructions to reset your password.'
                }
            except Exception as e:
                print('-------',e)
                response.data = {
                    'message': 'An error occurred while sending the email. Please try again later.'
                }
        else:
            response.data = {
                'message': 'No user with the provided email address was found.'
            }
        return response

class ChangePassword(APIView):
    def post(self,request):
        token = request.COOKIES['jwt']
        decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        id = decoded_token['id']
        user = Users.objects.get(id=id)
        email = user.email
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        user = Users.objects.get(email=email)
        response = Response()
        if user is not None:
            try:
                user.set_password(confirm_password)
                user.save()
                response.data = {
                'message': 'Password Set'
                }
            except Exception as e:
                print('-------',e)
                response.data = {
                    'message': 'Password  not Set'
                }
        else:
            response.data = {
                'message': 'No user with the provided email address was found.'
            }
                
        return response

class authenticate_user(APIView):
    def get(self, request):
        try:
            token = request.data['token']
            idInfo = id_token.verify_oauth2_token(token, requests.Request())
            email = idInfo['email']
            google_id = idInfo['sub']
            user_name = idInfo['user_name']
            response = Response()

            # check if user already exists
            user = Users.objects.filter(email=email).first()
            if user:
                response.data = {'message': 'User already exists'}
                return response
            else:
                # create a new user using the token info
                serializer = UserSerializer(data=request.data, context={'email': email, 'google_id': google_id, 'user_name': user_name})
                serializer.is_valid(raise_exception=True)
                serializer.save(email=email, user_name=user_name, google_id=google_id)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            response = Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return response
        except google.auth.exceptions.ExpiredTokenError:
            response = Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
            return response


# class confirmRegistration(APIView):
#     def get(self, request):
#         print('---------------------------------')
#         # print(request)
#         # user = User.objects.filter(token=request.data).first()
#         response = Response()

#         # if request is not None:
#         #     # request.is_active = True
#         #     # user.save()
#         #     response.data = {'message': 'User already exists'}
#         #     return response
#         #     # Redirect to the login page with a success message
#         #     # return redirect('login')
#         # else:
#         #     # Show an error message
#         #     response.data = {'message': 'User already exists'}
#         #     return response
        
#         response.data = {'message': 'User already exists'}
#         # return response
#         return response


class confirmRegistration(APIView):
    def post(self, request,token):
        # Retrieve the form
        print('token',token)
        token = request.query_params.get('token')

        print('====',token)
        signup_token = SignupToken.objects.filter(token=token).first()
        print('--------',signup_token)
        if signup_token is not None:
            context={'user_name': signup_token.user_name, 'email':signup_token.email, 'password':signup_token.password}
            print('context',context)
            serializer = UserSerializer(data=context )
            serializer.is_valid(raise_exception=True)
            serializer.save(user_name=signup_token.user_name, email=signup_token.email, password=signup_token.password)
            signup_token.delete()
            return redirect('http://localhost:4200/auth/login')
            # return Response({'message': 'Your registration has been confirmed and you can now log in.'})
        else:
            # Return an error response
            return redirect('http://localhost:4200/auth/login')
            # return Response({'message': 'Invalid or expired confirmation link.'})


class activate(APIView):
    def post(self,request, token): 
        print('token',token)
        print(request.POST)
        csrf_token = request.query_params.get('csrfmiddlewaretoken')
        response = Response()
        response.data = {'message': 'User already exists'}
        
        return response
        # User = get_user_model()  
    # try:  
    #     user = User.objects.get(pk=uid)  
    # except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
    #     user = None  
    # if user is not None and account_activation_token.check_token(user, token):  
    #     user.is_active = True  
    #     user.save()  
    #     return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    # else:  
    #     return HttpResponse('Activation link is invalid!')  



class UserListView(APIView):
    def get(self, request):
        users = Users.objects.all()  # Retrieve all users from the Users model
        print('users')
        serializer = UserSerializer(users, many=True)  # Serialize the users if needed
        return Response(serializer.data)  # Return the serialized data as the API response
