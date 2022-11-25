import pymongo

if __name__ == "__main__":
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    #print(client)
    db=client["SIH"]
    collection=db["Feedback"]
    
    def feedback(sub, des):
       
       dictionary={"Subject":sub, "Description":des}
       collection.insert_one(dictionary)