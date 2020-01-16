from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oauth2_provider.models import AccessToken
from rest_framework.views import APIView, Request, Response


@method_decorator(csrf_exempt, name='dispatch')
class LogInForOAuth2(View):
    def get(self, request):
        return render(request, template_name='auth_app/login.html')

    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            import json
            return HttpResponseBadRequest(json.dumps({'error': 'wrong form data'}))
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect(request.get_raw_uri())
        login(request, user)
        print(f'http://{request.get_host()}{request.GET["next"]}')
        ret = redirect(f'http://{request.get_host()}{request.GET["next"]}')
        return ret


class GetUserInfoView(APIView):
    def get(self, request):
        try:
            tok = request.META.get('HTTP_AUTHORIZATION', '')[7:]
            _ = AccessToken.objects.get(token=tok)
        except AccessToken.DoesNotExist:
            return Response(status=403)
        return Response(status=200)

