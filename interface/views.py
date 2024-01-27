# """ interface/views.py """"

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from wtforms import Form, StringField, IntegerField
from .models import db, DynamicModel

def home(request):
    with db.connection, db.connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [record[0] for record in cursor.fetchall()]
    return {'tables': tables}

@view_config(route_name='table_view', renderer='templates/table_view.jinja2')
def table_view(request):
    table_name = request.params.get('table_name', '')
    dynamic_model = getattr(DynamicModel, table_name, None)
    if dynamic_model:
        table_data = dynamic_model.table_info.fetch_data()
        return {'table_data': table_data}
    else:
        return Response('Table not found', status=404)

@view_config(route_name='insert_view', renderer='templates/insert_view.jinja2')
def insert_view(request):
    table_name = request.params.get('table_name', '')
    dynamic_model = getattr(DynamicModel, table_name, None)
    if dynamic_model:
        table_columns = [col[0] for col in db.connection.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")]
    else:
        return Response('Table not found', status=404)

    class DynamicForm(Form):
        pass

    for column_name in table_columns:
        setattr(DynamicForm, column_name, StringField(label=column_name))

    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.validate():
            data = {column: getattr(form, column).data for column in table_columns}
            new_data = dynamic_model.insert_data(data)
            return Response(f'Data inserted successfully: {new_data}', status=201)
    else:
        form = DynamicForm()

    return {'form': form, 'table_name': table_name}