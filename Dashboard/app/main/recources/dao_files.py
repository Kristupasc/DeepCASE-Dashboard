from Dashboard.data.dao.dao import DAO
from Dashboard.app.main.recources.setters_getters_cluster import *


def get_files():
    """
    Methode that returns all files in the database.

    Returns
    -------
    dataframe with all files.
    """
    dao = DAO()
    return dao.get_all_files()


def switch_file(value):
    """
    Methode that sets new file.
    Parameters
    -------
    The value the filename that needs to be put in the database.
    Returns
    -------
    dataframe with all files.
    """
    dao = DAO()
    return dao.switch_current_file(value)



def get_status_file():
    """
    file status as boolean
    Returns
    -------
    returns file status as boolean

    """
    dao = DAO()
    return dao.get_run_status()
def is_file_selected():
    """
    Check if a file is selected.

    Returns
    -------
    bool
        True if a file is selected, False otherwise.
    """
    dao = DAO()
    return 'emptyfile' != dao.display_selected_file()

