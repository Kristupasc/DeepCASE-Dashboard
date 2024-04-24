from Dashboard.data.dao.dao import DAO
from Dashboard.app.main.recources.loaddata import *


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


def get_initial_table():
    """
    Methode that returns the table that is uploaded

    Returns
    -------
    dataframe with file content
    """
    dao = DAO()
    return dao.get_initial_table()


def get_status_file():
    """
    file status as boolean
    Returns
    -------
    returns file status as boolean

    """
    dao = DAO()
    return dao.get_run_status()
