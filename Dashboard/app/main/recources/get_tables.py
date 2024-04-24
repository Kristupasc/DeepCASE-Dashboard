from Dashboard.data.dao.dao import DAO


def get_initial_table():
    """
    Methode that returns the table that is uploaded

    Returns
    -------
    dataframe with file content
    """
    dao = DAO()
    return dao.get_initial_table()