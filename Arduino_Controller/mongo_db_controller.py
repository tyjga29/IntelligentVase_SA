import pymongo
import yaml
import os


# MongoDB connection details
dir_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(dir_path, 'resources_package/mongo_db_param.yaml')
with open(yaml_path, 'r') as f:
    data = yaml.safe_load(f)
    mongo_param = data["mongo_db_param"]

URI = mongo_param["URI"]
DATABASE_NAME = mongo_param["DATABASE_NAME"]
COLLECTION_NAME = mongo_param["COLLECTION_NAME"]

CERTIFICATE_PATH = "resources_package/certificate_test_user.pem"

def send_light_to_mongodb(value):
    try:
        client = pymongo.MongoClient(URI, ssl_ca_certs=CERTIFICATE_PATH)
        
        db = client[DATABASE_NAME]
        
        collection = db[COLLECTION_NAME]

        data = {"LightInput": value}
        
        collection.insert_one(data)
        
    except Exception as e:
        print("Error:", e)