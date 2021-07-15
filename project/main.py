from src.datamanager import DataManagerWebSocket, DataManagerApi
from src.util import get_environment_variables, create_log, create_database

if __name__ == "__main__":
    environment_variables = get_environment_variables("./environment/env.json")
    create_log('Service Start', environment_variables['log_path'])
    create_database(environment_variables['database_destiny'], environment_variables['log_path'])
    dm = DataManagerWebSocket(environment_variables)
    dm.fetch_new_data()
