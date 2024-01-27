# Function to get a list of tables
def get_tables_list(engine):
    query = "SELECT shared.extract_visible_table() as table"
    result = engine.execute(query)
    tables = [row['table'] for row in result]
    return tables

# Function to get table structure
def get_table_structure(engine, table_name):
    query = f"SELECT * FROM shared.extract_table_columns('{table_name}')"
    result = engine.execute(query)
    columns = [dict(row) for row in result]
    return columns

# Function to get table data
def get_table_data(engine, table_name):
    query_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    result = engine.execute(query_tables)
    allowed_tables = [row['table_name'] for row in result]

    if table_name not in allowed_tables:
        return {"error": "Недопустимое имя таблицы"}, 400

    query = f"SELECT * FROM {table_name}"
    result = engine.execute(query)
    data = [dict(row) for row in result]
    return data