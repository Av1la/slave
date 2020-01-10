

from app.workers.mpmailcheck import MPMailCheckWorker


def check_single_mail():

    worker = MPMailCheckWorker('felip3333333223232e@gmail.com')
    worker.start()
