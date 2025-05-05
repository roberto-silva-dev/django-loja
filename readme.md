
# Guia: Criando um Projeto Django com Autenticação via Sessão, Categorias e Produtos

Este guia mostra como criar um projeto Django chamado `core` com um app `loja`, contendo autenticação simples baseada em sessão e cadastro de categorias e produtos com relação entre eles.

## Pré-requisitos

- Python 3.x instalado
- Django instalado (`pip install django`)

## Criando o Projeto e o App
- Crie e abra uma pasta para o projeto na IDE

```bash
django-admin startproject core .
python manage.py startapp loja
```

## Configurações Iniciais

No `core/settings.py`:
- Adicione `'loja'` em `INSTALLED_APPS`
- Crie a constante `LOGIN_URL = '/login/'`
- Crie a constante `LOGIN_REDIRECT_URL = '/produtos/'`
- Crie a constante `LOGOUT_REDIRECT_URL = '/login/'`



Crie `loja/urls.py`:

```python
from django.urls import path
from .views import LoginUsuarioView, LogoutUsuarioView
from .views import CategoriaListView, CategoriaCreateView, ProdutoListView, ProdutoCreateView

urlpatterns = [
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('produtos/', ProdutoListView.as_view(), name='produto_list'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto_create'),
]
```

Inclua as URLs do app em `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loja.urls')),
]
```

## Modelos

Em `loja/models.py`:

```python
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
```

## Autenticação com Sessão

Em `loja/views.py`:

```python
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class LoginUsuarioView(LoginView):
    template_name = 'login.html'

class LogoutUsuarioView(LogoutView):
    next_page = reverse_lazy('login')
```

## Templates
- `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Loja{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Loja</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"><a class="nav-link" href="{% url 'categoria_list' %}">Categorias</a></li>
          <li class="nav-item"><a class="nav-link" href="{% url 'produto_list' %}">Produtos</a></li>
        </ul>
        <ul class="navbar-nav">
          {% if user.is_authenticated %}
            <li class="nav-item">
              <form action="{% url 'logout' %}" method="POST">
                {% csrf_token %}
                <button class="nav-link" href="" type="submit">Logout</button>
              </form>
            </li>
          {% else %}
            <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Login</a></li>
          {% endif %}
        </ul>
      </div>
    </div>
  </nav>
  <div class="container mt-4">
    {% block content %}{% endblock %}
  </div>
</body>
</html>
```

- `templates/categoria_list.html`

```html
{% extends 'base.html' %}
{% block title %}Categorias{% endblock %}
{% block content %}
<h2>Categorias</h2>
<a href="{% url 'categoria_create' %}" class="btn btn-primary mb-3">Nova Categoria</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>#</th>
      <th>Nome</th>
    </tr>
  </thead>
  <tbody>
    {% for categoria in object_list %}
      <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ categoria.nome }}</td>
      </tr>
    {% empty %}
      <tr>
        <td colspan="2">Nenhuma categoria cadastrada.</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

- `templates/produto_list.html`

```html
{% extends 'base.html' %}
{% block title %}Produtos{% endblock %}
{% block content %}
<h2>Produtos</h2>
<a href="{% url 'produto_create' %}" class="btn btn-primary mb-3">Novo Produto</a>
<table class="table table-striped">
  <thead>
    <tr>
      <th>#</th>
      <th>Nome</th>
      <th>Preço</th>
      <th>Categoria</th>
    </tr>
  </thead>
  <tbody>
    {% for produto in object_list %}
      <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ produto.nome }}</td>
        <td>R$ {{ produto.preco }}</td>
        <td>{{ produto.categoria.nome }}</td>
      </tr>
    {% empty %}
      <tr>
        <td colspan="4">Nenhum produto cadastrado.</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

- `templates/form.html`

```html
{% extends 'base.html' %}
{% block title %}Formulário{% endblock %}
{% block content %}
<h2>Formulário</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-success">Salvar</button>
  <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
</form>
{% endblock %}
```

- `templates/login.html`

```html
{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-4">
    <h2 class="mb-3">Login</h2>
    <form method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit" class="btn btn-primary">Entrar</button>
    </form>
  </div>
</div>
{% endblock %}
```



## CRUD de Categorias e Produtos (CBV)

Em `loja/views.py`:

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Categoria, Produto
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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
```

```bash
python manage.py makemigrations
python manage.py migrate
```

## Protegendo as Rotas

As views usam `LoginRequiredMixin`, e a configuração `LOGIN_URL` redireciona usuários não logados.

## Testes Rápidos

- Crie um superusuário com `python manage.py createsuperuser`
- Teste login, cadastro de categorias e produtos.

## Conclusão

Você agora tem um projeto Django com autenticação via sessão e CRUD de categorias e produtos com relacionamento. Para evoluir:
- Adicione paginação e filtros
- Use Django Admin para testes rápidos
- Implemente edição e exclusão de registros
