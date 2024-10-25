# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template("landing_page/home.html")
    context = {""}
    return HttpResponse("Home")


def projects(request):
    return HttpResponse("Projects")


def contact(request):
    return HttpResponse("Contact")


def about(request):
    return HttpResponse("About")
