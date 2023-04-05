import os
SECRET_KEY = b'@\xcf\xaaO\x8d\xdd\x977\xbe\x00\x85\xdfRxK\xf5'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_1688_exam:QwertY000@std-mysql.ist.mospolytech.ru/std_1688_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMIN_ROLE_ID = 1
MODER_ROLE_ID = 2
USER_ROLE_ID = 3
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')