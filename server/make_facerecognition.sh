g++ facerecognition.cpp -o facerecognition `pkg-config --libs --cflags opencv` -ldl `mysql_config --cflags --libs` -O
