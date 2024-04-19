from datetime import time
from threading import Thread

from Dashboard.processing.process_split import ProcessorAccessObject
process_going_on = False

def start_deepcase():
    """
    Methode that runs deepcase on a different thread.
    Another thread takes care of the terminations.
    This design fix a bug in Dash, that appear on multiple pages.
    Returns
    -------
    void
    """
    global process_going_on
    process_going_on = True
    pao = ProcessorAccessObject()
    thread = Thread(target=pao.run_DeepCASE())
    thread.start()
    thread2 = Thread(target=check_thread_alive(thread))
    thread2.start()

def start_automatic():
    """
    Runs automatic analysis.
    This use a thread in order to keep it running in background.
    Known bug in Dash.
    Returns
    -------
    object ProcessorAccessObject that runs automatic analysis
    """
    global process_going_on
    process_going_on = True
    pao = ProcessorAccessObject()
    thread = Thread(target=pao.run_automatic_mode())
    thread.start()
    thread2 = Thread(target=check_thread_alive(thread))
    thread2.start()
    return pao
def check_thread_alive(thread):
    """
    Methode that should be run on a separate thread.
    It simply checks if thread alive and does a final action.
    Parameters
    ----------
    thread Is the thread where we check on if it is alive.
    When it is dead we signal that it is done.

    Returns
    -------
    is void because the signal is the last thing.

    """
    global process_going_on
    while(thread.is_alive()):
        time.sleep(2)
    process_going_on = False