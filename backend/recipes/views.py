from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'recipes/index.html'
    return render(request, template)


def recipe_list(request):
    return render(request, 'recipes/recipe-list.html')


def recipe_detail(request, pk):
    return render(request, 'recipes/recipe-detail.html')
