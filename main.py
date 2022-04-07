import threading

from Sequencing.Influenza import insert as influenza
from Sequencing.SARS import insert as sars

if __name__ == '__main__':
    inserts = 10000
    sars_t = threading.Thread(target=sars, args=(inserts,))
    influenza_t = threading.Thread(target=influenza, args=(inserts,))
    sars_t.start()
    influenza_t.start()
    sars_t.join()
    influenza_t.join()
