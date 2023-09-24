import firebase_admin
import firebase_admin.firestore

import requests



def callback_collection_on_snapshot(doc_snapshot, changes, read_time):
    try:
        print("Callback is called")
        print(read_time)
        for d in changes:
            command = d.document.to_dict()
            if "executed_at" not in command:
                command["executed_at"] = None
            if command["executed_at"] == None:
                collec.document(d.document.id).update({"executed_at" : firebase_admin.firestore.SERVER_TIMESTAMP})
                if "query_params" not in command:
                    command["query_params"] = dict()
                if ("method" not in command) or ("endpoint" not in command):
                    #Firestoreのフィールドが足りないよ
                    print("E: Insufficient Field")
                    collec.document(d.document.id).update({"status_code" : -1})
                else:
                    r = requests.request(command["method"], "http://192.168.100.65:8080/" + command["endpoint"], data = command["query_params"])
                    collec.document(d.document.id).update({"status_code" : r.status_code})
                    print(r, "Done")
            else:
                print("skip")
    except Exception as e:
        print("E:", e)




#firestoreよみぶのしょきか
cred = firebase_admin.credentials.Certificate("ind-hackz-tyranno-firebase-adminsdk-ue8h4-eeefe796a9.json")
firebase_admin.initialize_app(cred)
db = firebase_admin.firestore.client()
collec = db.collection("esp_commands_queue")
collec.on_snapshot(callback_collection_on_snapshot)

while True:
    pass