import face_recognition
import cv2
import numpy as np
from datetime import datetime
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image
import io
from tempfile import NamedTemporaryFile
from api_keys import MongoDBURL
def face_login():
    
    user_name = input("Enter User name: ")
    user_data = retrieve()
    
    video_capture = cv2.VideoCapture(0)

    User_face_encoding = []
    User_face_name = []
    is_find=False
    try:
        for user_info in user_data:
            name = user_info["name"]
            if name==user_name:
                temp_image = NamedTemporaryFile(delete=False, suffix=".jpg")
                user_info["Face"].save(temp_image, format="JPEG")
                temp_image_path = temp_image.name

                face_image = face_recognition.load_image_file(temp_image_path)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                
                User_face_encoding.append(face_encoding)
                User_face_name.append(name)

                temp_image.close()
                os.remove(temp_image_path)
                is_find=True
        if not is_find:
            print("User Not Found")
            return False
    except:
        print("Face Retrivel from DataBase Failed !")
        

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    try:
        while True:
            _, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(User_face_encoding, face_encoding)
                face_distance = face_recognition.face_distance(User_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = User_face_name[best_match_index]
                        
                    if name == user_name:
                        return name
            cv2.imshow("Face Login: ", frame)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()
        return False
    except Exception as e:
        print(e)


def load():
    uri = MongoDBURL
    
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        
    mydb = client["Employee_Login"]
    mycol = mydb["Persons"]
    
    pa=r"C:\Users\Administrator\OneDrive\Pictures\Camera Roll\WIN_20230827_16_45_30_Pro.jpg"
    username="Fuzail"
    try:
        image = Image.open(pa)

        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_binary = image_bytes.getvalue()
    except :
        print("Image Processing Failed")
    
    mylist = { "name": username, "Face":image_binary}
    try:
        if( mycol.find_one({'name':username}) | mycol.find_one({'Face':image_binary}) ):
            print("User Already Exists")
        else:
            mycol.insert_one(mylist)
    except:
            mycol.insert_one(mylist)
        
    client.close()
    
    
def retrieve():
    uri = MongoDBURL
    
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        
    try:
        db = client['Employee_Login']
        collection = db['Persons']
        
        collections=collection.find()
        users = []
        for collection in  collections:
            
            retrieved_image = Image.open(io.BytesIO(collection['Face']))
            user_name = {
                "name": collection["name"],
                "Face": retrieved_image
            }
            
            users.append(user_name)

        client.close()
        return users
    except:
        print("Data Retrievel Failed")

if __name__=='__main__':
    print(face_login())

