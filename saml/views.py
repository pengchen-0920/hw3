from http.client import HTTPResponse
from django.conf import settings
from django.urls import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.shortcuts import render

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    # print(request.META['HTTP_HOST'])
    # print(request.META['PATH_INFO'])
    # print(request.is_secure())
    result = {
        # 'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': False,
        'post_data': request.POST.copy()
    }
    print('result', result)
    return result

# redirect 到助教登入的服務（settings.py > idp > singleSignOnService > url）
def sso(request):
    print('enter sso function!')
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    print('auth.login()', auth.login())
    return HttpResponseRedirect(auth.login())

# 接收助教 server 傳回來的 login response，資料存進 session
def acs(request):
    print('enter acs function!')
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    auth.process_response() # parse SAMLResponse(xml format)
    errors = auth.get_errors()
    if not errors:
        if auth.is_authenticated():
            request.session['samlUserdata'] = auth.get_attributes()
            request.session['samlNameId'] = auth.get_nameid()
            request.session['samlNameIdFormat'] = auth.get_nameid_format()
            request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            request.session['samlSessionIndex'] = auth.get_session_index()
            print(f"==Request Session: {request.session.items()}")
        else:
            print('Not authenticated')
    else:
        print("Error when processing SAML Response: %s %s" % (', '.join(errors), auth.get_last_error_reason()))

    return HttpResponseRedirect('http://127.0.0.1:8000/')


# redirect 到助教登出的服務（settings.py > idp > singleLogoutService > url）
def slo(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)

    name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
    if 'samlNameId' in request.session:
        name_id = request.session['samlNameId']
    if 'samlSessionIndex' in request.session:
        session_index = request.session['samlSessionIndex']
    if 'samlNameIdFormat' in request.session:
        name_id_format = request.session['samlNameIdFormat']
    if 'samlNameIdNameQualifier' in request.session:
        name_id_nq = request.session['samlNameIdNameQualifier']
    if 'samlNameIdSPNameQualifier' in request.session:
        name_id_spnq = request.session['samlNameIdSPNameQualifier']
    return HttpResponseRedirect(auth.logout(name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format, spnq=name_id_spnq))

# 接收助教 server 傳回來的 logout response
def sls(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    request_id = None
    if 'LogoutRequestID' in request.session:
        request_id = request.session['LogoutRequestID']
    dscb = lambda: request.session.flush()
    url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
    errors = []
    errors = auth.get_errors()

    if len(errors) == 0:
        if url is not None:
            # To avoid 'Open Redirect' attacks, before execute the redirection confirm
            # the value of the url is a trusted URL
            return HttpResponseRedirect(url)
        else:
            success_slo = True
            return HttpResponseRedirect('http://127.0.0.1:8000/')
    elif auth.get_settings().is_debug_active():
        error_reason = auth.get_last_error_reason()
        print(error_reason)


def metadata(request):
    saml_settings = OneLogin_Saml2_Settings(settings=None, custom_base_path=settings.SAML_FOLDER, sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp
