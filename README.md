# realtimeFaceRecognition
## Set up for Python
1. Install Python or run it on virtual env (version 3.8) : ([Download](https://www.python.org))

2. Install all Python packages in file "Reference.txt"


## Set up C compiler for Desktop App:
1. Install Visual Studio Community Ver
2. Select Desktop development with C++ in Visual Studio Installer

![image](https://github.com/user-attachments/assets/3a24dee2-32ef-478f-824d-162489509408)


## Set up for DataBase
1. Create a database on Firebase ([FireBase](https://console.firebase.google.com/u/0/))
2. Create Realtime Database and Storage:

![image](https://github.com/user-attachments/assets/940b8b0b-84e2-47a8-9b29-7b7a310c069d)

3. Generate a private key in Firebase:

![image](https://github.com/user-attachments/assets/c6a95a1f-2137-432a-9256-33e6b265092e)

4. Rename it to serviceAccountKey.json
5. Copy this file to Project
6. Change cred = credentials.Certificate(path to serviceAccountKey.json location) in main.py
7. Change url database, storageBucket in firebase_admin.initialize_app(...)

## Run Application
1. Run file main.py to start application
2. Run the files AddDatatoDatabase.py and Encode Generator.py respectively to upload new data to the database
