# """ main.py """"

from config import main

if __name__ == '__main__':
    with Configurator() as config:
        engine = con.pgCon_postgres()
        table_names = fun.get_tables_list(engine)

        api.spawn_actions(config, table_names)

        app = main(global_config, **settings)
        server = make_server('0.0.0.0', 6543, app)
        server.serve_forever()