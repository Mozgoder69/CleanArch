from sqlalchemy import create_engine

# Function to connect to PostgreSQL
def connect_to_postgres(uname, pword):
    return create_engine(f'postgresql://{uname}:{pword}@localhost:1618/cleaners')

def pgCon_customer():
    return connect_to_postgres('customer', 'customer')

def pgCon_master():
    return connect_to_postgres('tema21904', 'tema21904')

def pgCon_operator():
    return connect_to_postgres('teop31803', 'teop31803')

def pgCon_admin():
    return connect_to_postgres('tead41702', 'tead41702')

def pgCon_leader():
    return connect_to_postgres('tele51601', 'tele51601')

def pgCon_postgres():
    return connect_to_postgres('postgres', '1618')