from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def log_in(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/')
				else:
					return render_to_response('', context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/login/')
	else:
		formulario = AuthenticationForm()
	return render_to_response('autenticacion/login.html', {formulario: formulario},
			context_instance=RequestContext(request))


@login_required(login_url='/login/')
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/login/')
