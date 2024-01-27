# """ endpoints.py """"

def spawn_actions(config, table_names):
    for table in table_names:
        config.add_route(f'{table}_select', f'/{table}/select')
        config.add_route(f'{table}_insert', f'/{table}/insert')
        config.add_route(f'{table}_update', f'/{table}/update/{id}')
        config.add_route(f'{table}_delete', f'/{table}/delete/{id}')