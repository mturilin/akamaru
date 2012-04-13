from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from akamaru.app_settings import RESOLVE_FORM_KEY, WORKFLOW_SESSION_KEY, LOGIN_OK_KEY, LOGIN_ERROR_KEY, OPERATION_KEY, OPERATION_LOGIN, OPERATION_ASSOCIATE

__author__ = 'mturilin'


class BackendError(StandardError):
    pass


def get_callback_url(backend_name):
    return reverse("akamaru-callback", args=(backend_name,))

def get_resolve_url():
    return reverse("akamaru-resolve")


class AkamaruBackend(object):
    def get_login_url(self, request):
        raise NotImplementedError()

    def create_social_user(self, user, session):
        raise NotImplementedError()

    def get_backend_name(self):
        raise NotImplementedError()

    def get_redirect_url(self, request):
        return request.build_absolute_uri(get_callback_url(self.get_backend_name()))


class AkamaruError(StandardError):
    pass

_backend_dict = None

def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_backend_dict():
    global _backend_dict

    if not _backend_dict:
        backend_str_list = getattr(settings, "AUTHENTICATION_BACKENDS")
        backend_class_list = [get_class(class_name) for class_name in backend_str_list]
        backend_list = [a_class() for a_class in backend_class_list if issubclass(a_class, AkamaruBackend)]
        _backend_dict = dict((backend.get_backend_name(), backend) for backend in backend_list)

    return _backend_dict


class AkamaruError(StandardError):
    pass


def get_workflow(request):
    if WORKFLOW_SESSION_KEY not in request.session:
        raise AkamaruError("Session middleware is not set up")
    workflow = request.session[WORKFLOW_SESSION_KEY]
    return workflow


def set_workflow(request, workflow):
    request.session[WORKFLOW_SESSION_KEY] = workflow


def login_ok_redirect():
    return redirect(reverse(settings.AKAMARU_LOGIN_OK))