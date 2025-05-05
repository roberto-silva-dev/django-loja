from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Categoria, Produto
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginUsuarioView(LoginView):
    template_name = 'login.html'

class LogoutUsuarioView(LogoutView):
    next_page = reverse_lazy('login')

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'categoria_list.html'

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nome']
    success_url = reverse_lazy('categoria_list')
    template_name = 'form.html'

# Mesma lógica para Produto
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto_list.html'

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome', 'preco', 'categoria']
    success_url = reverse_lazy('produto_list')
    template_name = 'form.html'