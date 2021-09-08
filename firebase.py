# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class MyDataBase:
    def __init__(self) -> None:
        cred = credentials.Certificate("./dbkey.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create(self, collection, data, docID=None) -> dict:
        try:
            if docID != None:
                doc_ref = self.db.collection(collection).document(docID)
                doc_ref.set(data)
            else:
                doc_ref = self.db.collection(collection)
                doc_ref.add(data)
            res = {'msg': 'create success',
                   'data': data
                   }
        except Exception as err:
            res = {'msg': f'create failed: {err}',
                   'data': data
                   }
        return res

    def read(self, collection, docID) -> dict:
        try:
            doc_ref = self.db.collection(collection).document(docID)
            doc = doc_ref.get()
            if doc.exists:
                res = {'msg': 'get document success',
                       'data': doc.to_dict()
                       }
            else:
                res = {'msg': 'document not exists'}
        except Exception as err:
            res = {'msg': err}

        return res

    def update(self, collection, data, docID) -> dict:
        try:
            doc_ref = self.db.collection(collection).document(docID)
            doc_ref.update(data)
            res = {'msg': 'update success',
                   'data': data
                   }
        except Exception as err:
            res = {'msg': err}
        return res

    def delete(self, collection, docID) -> None:
        try:
            doc_ref = self.db.collection(collection).document(docID)
            doc_ref.delete()
            res = {'msg': 'delete success'}
        except Exception as err:
            res = {'msg': err}
        return res
