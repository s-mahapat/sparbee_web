import os
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request=request, template_name="index.html")

def template(request, tmpl_name):
    tmpl_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates", tmpl_name + ".html")
    return render(request=request, template_name=tmpl_file)