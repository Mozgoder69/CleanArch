# """ __init__.py """"

from wsgiref.simple_server import make_server
from pyramid.httpexceptions import HTTPFound
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import engine_from_config, inspect
from pyramid.renderers import render_to_response

@view_config(route_name='add_user', request_method='GET', renderer='templates/add_user.jinja2')
def add_user_get(request):
    columns = [col.name for col in inspect(User).c if col.name != 'id']
    return {'columns': columns}

@view_config(route_name='add_user', request_method='POST')
def add_user_post(request):
    new_user = User()
    for column in inspect(User).c:
        if column.name != 'id':
            setattr(new_user, column.name, request.POST.get(column.name))
    request.dbsession.add(new_user)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='auth', renderer='../../templates/auth.html')
def hello_world(request):
    return render_to_response('auth.html', {}, request=request)