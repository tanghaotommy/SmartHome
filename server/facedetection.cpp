#include </home/ec2-user/opencv-2.4.13/modules/contrib/include/opencv2/contrib/contrib.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/core/include/opencv2/core/core.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/highgui/include/opencv2/highgui/highgui.hpp>
#include "/home/ec2-user/opencv-2.4.13/include/opencv/cv.h"
#include <fstream>
#include <pthread.h>
using namespace std;
using namespace cv;

#define NUM_THREADS 4

CascadeClassifier haarcascade_frontalface_alt;
CascadeClassifier haarcascade_frontalface_alt2;
CascadeClassifier haarcascade_frontalface_alt_tree;
CascadeClassifier haarcascade_frontalface_default;
bool detected[NUM_THREADS] = {false};

void *haarcascade_frontalface_alt_detect(void *pic)
{
    const char *haarcascade_frontalface_alt_name = "./FaceData/haarcascade_frontalface_alt.xml";
    if( !haarcascade_frontalface_alt.load( haarcascade_frontalface_alt_name ) )
    { 
        cout << "ERROR: Could not load classifier haarcascade_frontalface_alt\n";
        exit(-1); 
    }
    vector<Rect> haarcascade_frontalface_alt_objs;
    haarcascade_frontalface_alt.detectMultiScale(*((Mat*)pic), haarcascade_frontalface_alt_objs);
    detected[0] = haarcascade_frontalface_alt_objs.size();
    //cout << "haarcascade_frontalface_alt: " << haarcascade_frontalface_alt_objs.size() << endl;
}

void *haarcascade_frontalface_alt2_detect(void *pic)
{
    const char *haarcascade_frontalface_alt2_name = "./FaceData/haarcascade_frontalface_alt2.xml";
    if( !haarcascade_frontalface_alt2.load( haarcascade_frontalface_alt2_name ) )
    { 
        cout << "ERROR: Could not load classifier haarcascade_frontalface_alt2\n";
        exit(-1); 
    }
    vector<Rect> haarcascade_frontalface_alt2_objs;
    haarcascade_frontalface_alt2.detectMultiScale(*((Mat*)pic), haarcascade_frontalface_alt2_objs);
    detected[1] = haarcascade_frontalface_alt2_objs.size();
    //cout << "haarcascade_frontalface_alt2: " << haarcascade_frontalface_alt2_objs.size() << endl;
}

void *haarcascade_frontalface_alt_tree_detect(void *pic)
{
    const char *haarcascade_frontalface_alt_tree_name = "./FaceData/haarcascade_frontalface_alt_tree.xml";
    if( !haarcascade_frontalface_alt_tree.load( haarcascade_frontalface_alt_tree_name ) )
    { 
        cout << "ERROR: Could not load classifier haarcascade_frontalface_alt_tree\n";
        exit(-1); 
    }
    vector<Rect> haarcascade_frontalface_alt_tree_objs;
    haarcascade_frontalface_alt_tree.detectMultiScale(*((Mat*)pic), haarcascade_frontalface_alt_tree_objs);
    detected[2] = haarcascade_frontalface_alt_tree_objs.size();
    //cout << "haarcascade_frontalface_alt_tree: " << haarcascade_frontalface_alt_tree_objs.size() << endl;
}

void *haarcascade_frontalface_default_detect(void *pic)
{
    const char *haarcascade_frontalface_default_name = "./FaceData/haarcascade_frontalface_default.xml";
    if( !haarcascade_frontalface_default.load( haarcascade_frontalface_default_name ) )
    { 
        cout << "ERROR: Could not load classifier haarcascade_frontalface_default\n";
        exit(-1); 
    }
    vector<Rect> haarcascade_frontalface_default_objs;
    haarcascade_frontalface_default.detectMultiScale(*((Mat*)pic), haarcascade_frontalface_default_objs);
    detected[3] = haarcascade_frontalface_default_objs.size();
    //cout << "haarcascade_frontalface_default: " << haarcascade_frontalface_default_objs.size() << endl;
}

int main(int argc, char **argv)
{
    char *file_dir = argv[1];
    
    Mat pic = imread(file_dir, CV_LOAD_IMAGE_GRAYSCALE);

    pthread_t threads[NUM_THREADS];
    int i = 0;
    int rc = pthread_create(&threads[i++], NULL, haarcascade_frontalface_alt_detect, (void *)&pic);
    if (rc)
    {         
        cout << "Error:unable to create thread," << rc << endl;         
        exit(-1);      
    }
    rc = pthread_create(&threads[i++], NULL, haarcascade_frontalface_alt2_detect, (void *)&pic);
    if (rc)
    {         
        cout << "Error:unable to create thread," << rc << endl;         
        exit(-1);      
    }
    rc = pthread_create(&threads[i++], NULL, haarcascade_frontalface_alt_tree_detect, (void *)&pic);
    if (rc)
    {         
        cout << "Error:unable to create thread," << rc << endl;         
        exit(-1);      
    }
    rc = pthread_create(&threads[i++], NULL, haarcascade_frontalface_default_detect, (void *)&pic);
    if (rc)
    {         
        cout << "Error:unable to create thread," << rc << endl;         
        exit(-1);      
    }

    pthread_join(threads[0],NULL); 
    pthread_join(threads[1],NULL); 
    pthread_join(threads[2],NULL); 
    pthread_join(threads[3],NULL);  

    int count = 0;
    for(int i = 0; i < NUM_THREADS; i++)
    {
        if(detected[i])
            ++count;
    }
    if(count > NUM_THREADS / 2)
        cout << true << endl;
    else
        cout << false << endl;

    return 0;
}
