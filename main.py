from google.cloud import firestore, exceptions
from datetime import datetime
from my_fun import ts2str, str2ts
from my_fun import get_data, avail_begin, ada_avail, avail_end

#  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path  If not set, set here
products = {"8GB": "5813", "4GB": "5812"}
# collection = "test-avail"  # test collection
collection = "rpi5-avail"  # production collection
db = firestore.Client()
for product in products:
    doc_ref = db.collection(collection).document(product)
    data = get_data(doc_ref)
    avail = ada_avail(products[product])
    ###########################################################################
    ###########################################################################
    if not avail and data["status"] == "inactive":  # product still unavailable
        continue
    if avail and data["status"] == "active":  # product still available
        continue
    if avail and data["status"] == "inactive":  # prod  was unavail, now it's avail
        avail_begin(doc_ref, data)
        continue
    if not avail and data["status"] == "active":  # prod was avail, now it's not
        avail_end(doc_ref, data, product)
        continue
###############################################################################
