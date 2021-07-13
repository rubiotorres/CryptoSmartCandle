from src.datamanager import DataManagerWebSocket
from src.util import get_environment_variables

if __name__ == "__main__":
    environment_variables = get_environment_variables()

    dm = DataManagerWebSocket(environment_variables)
    dm.fetch_new_data()
