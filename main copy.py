# imports
from constants import products
from my_fun import avail_end, get_data, ts2str, write_data
from datetime import datetime
from google.cloud import firestore

# constants
collection = "test-Avail"
db = firestore.Client()

# main
for product in products:
    doc_ref = db.collection(collection).document(product)
    data = get_data(doc_ref)
    ############################################################################
    ############################################################################
    # product was unavail, and is still unavail, do nothing
    if not data["status"] == "active":
        continue
    # product was avail, and is still avail, do nothing
    if data["status"] == "active":
        continue
    # product was unavail, and now it's avail, start the avail period
    if data["status"] == "inactive":
        data["begin-time"] = ts2str(datetime.now())
        data['begin-time-ts'] = datetime.now()
        data["status"] = "active"
        write_data(doc_ref, data)
        continue
    # product was avail, and now it's unavail, shut down the avail period
    if data["status"] == "active":
        avail_end(doc_ref, data)
        continue
###############################################################################

# data = get_data(db, '8GB')
# data['begin-time'] = ts2str(datetime.now())
# data['status'] = 'inactive'
# write_data(db, '8GB', data)

# test(db)
pass
