from datetime import datetime, timedelta
import requests
import json

# move the following imports to main as needed
# from google.cloud import firestore, exceptions
# from my_fun import  ts2str
# from my_fun import  str2ts
# from my_fun import get_data, write_data


def ts2str(timestamp):
    """Convert a Python datetime object to a human-readable string."""
    # 2023-11-08 09:59:58
    # Format the timestamp to a string: YYYY-MM-DD HH:MM:SS
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def str2ts(human_readable):
    """Convert a human-readable string to a Python datetime object."""
    # 2023-11-08 09:59:58
    # Parse the string back to a datetime object
    # This function assumes the string format is the same as the one provided by timestamp_to_human_readable
    return datetime.strptime(human_readable, "%Y-%m-%d %H:%M:%S")


def get_data(doc_ref):
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        dict = {
            "begin_time": "",
            "status": "inactive",
        }
        doc_ref.set(dict)
        return dict


def avail_begin(doc_ref, data):
    data["begin_time"] = ts2str(datetime.now())
    data["status"] = "active"
    doc_ref.set(data)


def write_data(doc_ref, data):
    doc_ref.set(data)


def td2str(delta):
    # Extract days
    days = delta.days
    # Extract seconds and convert to hours, minutes, seconds
    seconds = delta.seconds
    hours = seconds // 3600  # Integer division to get the number of hours
    seconds %= 3600  # Modulus operator to get the remaining seconds
    minutes = seconds // 60
    seconds %= 60  # Remaining seconds
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def avail_end(doc_ref, data, product):
    begin_time_obj = str2ts(data["begin_time"])
    begin_str = data["begin_time"]
    now = datetime.now()
    timedelta = now - begin_time_obj
    new_data = {
        "product": product,
        "begin_time": begin_str,
        "end_time": ts2str(now),
        "duration": td2str(timedelta),
    }
    newdoc_ref = doc_ref.collection("avail-periods").document(begin_str)
    newdoc_ref.set(new_data)
    data["status"] = "inactive"
    data["begin_time"] = ""
    doc_ref.set(data)
    return True


def ada_avail(product):
    # product = '5813'
    url = "https://www.adafruit.com/api/product/" + product
    response = requests.get(url)
    avail = response.json()["product_stock"]
    if avail == "in stock":
        return True
    elif int(avail) > 0:
        return True
    return False
