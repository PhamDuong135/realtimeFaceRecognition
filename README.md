# realtimeFaceRecognition
## Set up for Python
1. Install Python or run it on virtual env (version 3.8) : ([Download](https://www.python.org))

2. Install all Python packages in file "Reference.txt"


## Set up C compiler for Desktop App:
1. Install Visual Studio Community Ver
2. Select Desktop development with C++ in Visual Studio Installer

## Set up for DataBase
1. Create a database on Firebase ([FireBase](https://console.firebase.google.com/u/0/))
2. Generate a private key in Firebase
3. Rename it to serviceAccountKey.json
4. Copy this file to Project
5. Change cred = credentials.Certificate(path to serviceAccountKey.json location) in main.py
6. Change url database, storageBucket in firebase_admin.initialize_app(...)

## Run Application
1. Run file main.py to start application
2. Run the files AddDatatoDatabase.py and Encode Generator.py respectively to upload new data to the database
