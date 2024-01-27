# """ config.py """"

from pyramid.config import Configurator

def setup_routes(config, engine):
    config.add_route('home', '/')
    config.add_view(home, route_name='home', renderer='templates/home.jinja2')
    config.add_route('table_view', '/table_view')
    config.add_view(table_view, route_name='table_view', renderer='templates/table_view.jinja2')
    config.add_route('insert_view', '/insert_view')
    config.add_view(insert_view, route_name='insert_view', renderer='templates/insert_view.jinja2')

def setup_views(config, engine):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("../../templates/", name='.html')

def main(global_config, **settings):
    config = Configurator(settings=settings)

    setup_routes(config, engine)
    setup_views(config, engine)

    return config.make_wsgi_app()