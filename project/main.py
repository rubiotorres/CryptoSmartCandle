from src.datamanager import DataManagerWebSocket, DataManagerApi
from src.util import get_environment_variables

if __name__ == "__main__":
    environment_variables = get_environment_variables("./environment/env.json")
    dm = DataManagerApi(environment_variables)
    dm.fetch_new_data()
