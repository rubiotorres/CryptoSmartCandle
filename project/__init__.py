from src.datamanager import DataManagerWebSocket
from src.util import get_environment_variables, createTables

from src.queries import sqlCreateTable

if __name__ == "__main__":
    environment_variables = get_environment_variables()
    # Create Table
    createTables(environment_variables['database_destiny'], environment_variables['table_destiny'], sqlCreateTable)
    dm = DataManagerWebSocket(environment_variables)
    dm.fetch_new_data()
