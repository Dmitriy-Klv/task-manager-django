from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if access_token:
            try:
                token = AccessToken(access_token)
                if datetime.utcfromtimestamp(token["exp"]) > datetime.utcnow():
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
                    return
            except TokenError:
                pass

            new_access = self._refresh_access_token(refresh_token)
            if new_access:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                request._new_access_token = new_access
        elif refresh_token:
            new_access = self._refresh_access_token(refresh_token)
            if new_access:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                request._new_access_token = new_access

    def process_response(self, request, response):
        new_access = getattr(request, "_new_access_token", None)
        if new_access:
            try:
                expiry = datetime.utcfromtimestamp(AccessToken(new_access)["exp"])
                response.set_cookie(
                    key="access_token",
                    value=new_access,
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    expires=expiry,
                )
            except TokenError:
                pass
        return response

    def _refresh_access_token(self, refresh_token):
        if not refresh_token:
            return None
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except TokenError:
            return None
