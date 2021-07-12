from project.src.datamanager import DataManagerWebSocket

if __name__ == "__main__":
    dm = DataManagerWebSocket([1, 5, 10])
    dm.fetch_new_data()
