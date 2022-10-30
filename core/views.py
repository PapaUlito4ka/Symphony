from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse


def home(request: HttpRequest):
    return redirect(reverse('admin:index'), permanent=True)
