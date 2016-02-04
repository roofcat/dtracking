# -*- coding: utf-8 -*-


import logging


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.shortcuts import render
from django.views.generic import TemplateView


class LoginRequiredMixin(object):

	@classmethod
	def as_view(self, **kwargs):
		view = super(LoginRequiredMixin, self).as_view(**kwargs)
		return login_required(view, login_url='/login/')


class ProfileTemplateView(LoginRequiredMixin, TemplateView):

	def get(self, request, *args, **kwargs):
		""" Root del template del perfil
		"""
		return render(request, 'autenticacion/profile.html')

	def post(self, request, *args, **kwargs):
		""" Método para cambiar la contraseña del usuario
		"""
		try:
			body = QueryDict(request.body)
			user = User.objects.get(pk=request.user.id)
			new_password1 = body.get('new_password1')
			new_password2 = body.get('new_password2')
			if new_password1 and new_password2 is not None:
				user.set_password(new_password1)
				user.save()
				return HttpResponse('Contraseña cambiada.', content_type='application/json')
			else:
				return HttpResponse('No se pudo cambiar la contraseña.', content_type='application/json')
		except Exception, e:
			logging.error(e)
			return HttpResponse(e)

	def patch(self, request, *args, **kwargs):
		""" Método para cambiar datos del usuario
		"""
		try:
			body = QueryDict(request.body)
			user = User.objects.get(pk=request.user.id)
			first_name = body.get('first_name')
			last_name = body.get('last_name')
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			return HttpResponse('Registro actualizado.', content_type='application/json')
		except Exception, e:
			logging.error(e)
			return HttpResponse(e)

profile = ProfileTemplateView.as_view()


def home_to_dashboard(request):
	return HttpResponseRedirect(reverse('dashboard:index'))

def log_in(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect(reverse('dashboard:index'))
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect(reverse('dashboard:index'))
				else:
					return HttpResponse("Usuario no activo")
			else:
				return HttpResponseRedirect('/login/')
	else:
		formulario = AuthenticationForm()
	return render(request, 'autenticacion/login.html', {formulario: formulario})

@login_required(login_url='/login/')
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/login/')
