from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
import os
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status

FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v8.0/oauth/access_token"
FACEBOOK_URL = "https://graph.facebook.com/"


class SignInView(APIView):
    def get(self, request):
        # get users access token from code in the facebook login dialog redirect
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={your-facebook-apps-id}&redirect_uri=http://localhost:8000/login/&client_secret={app_secret}&code={code-generated-from-login-result}
        user_access_token_payload = {
            "client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": "http://localhost:3000/login",
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": request.query_params.get("code"),
        }

        user_access_token_request = requests.get(
            FACEBOOK_ACCESS_TOKEN_URL, params=user_access_token_payload
        )
        user_access_token_response = json.loads(user_access_token_request.text)
        print(user_access_token_response)
        if "error" in user_access_token_response:
            user_access_token_error = {
                "message": "wrong facebook access token / this facebook access token is already expired."
            }
            return Response(user_access_token_error, status=status.HTTP_400_BAD_REQUEST)

        user_access_token = user_access_token_response["access_token"]

        # get developers access token
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={your-app-id}&client_secret={your-app-secret}&grant_type=client_credentials
        developers_access_token_payload = {
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "grant_type": "client_credentials",
        }
        developers_access_token_request = requests.get(
            FACEBOOK_ACCESS_TOKEN_URL, params=developers_access_token_payload
        )
        developers_access_token_response = json.loads(
            developers_access_token_request.text
        )

        if "error" in developers_access_token_response:
            developers_access_token_error = {
                "message": "Invalid request for access token."
            }
            return Response(developers_access_token_error, status=status.HTTP_400_BAD_REQUEST)

        developers_access_token = developers_access_token_response["access_token"]
        # inspect the users access token --> validate to make sure its still valid
        # https://graph.facebook.com/debug_token?input_token={token-to-inspect}&access_token={app-token-or-admin-token}

        verify_user_access_token_payload = {
            "input_token": user_access_token,
            "access_token": developers_access_token,
        }

        verify_user_access_token_request = requests.get(
            FACEBOOK_DEBUG_TOKEN_URL, params=verify_user_access_token_payload
        )
        verify_user_access_token_response = json.loads(
            verify_user_access_token_request.text
        )

        if "error" in verify_user_access_token_response:
            verify_user_access_token_error = {
                "message": "Could not verifying user access token."
            }
            return Response(verify_user_access_token_error)

        user_id = verify_user_access_token_response["data"]["user_id"]

        # get users email
        # https://graph.facebook.com/{your-user-id}?fields=id,name,email&access_token={your-user-access-token}
        user_info_url = FACEBOOK_URL + user_id
        user_info_payload = {
            "fields": "id,name,email",
            "access_token": user_access_token,
        }

        user_info_request = requests.get(
            user_info_url, params=user_info_payload)
        user_info_response = json.loads(user_info_request.text)

        users_email = user_info_response["email"]

        # create user if not exist
        try:
            user = User.objects.get(email=user_info_response["email"])
        except User.DoesNotExist:
            user = User()
            user.username = user_info_response["email"]
            # provider random default password
            user.password = make_password(
                BaseUserManager().make_random_password())
            user.email = user_info_response["email"]
            user.save()

        token = RefreshToken.for_user(
            user
        )  # generate token without username & password
        response = {}
        response["username"] = user.username
        response["access"] = str(token.access_token)
        response["refresh"] = str(token)
        return Response(response)
