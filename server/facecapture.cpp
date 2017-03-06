#include </home/ec2-user/opencv-2.4.13/modules/contrib/include/opencv2/contrib/contrib.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/core/include/opencv2/core/core.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/highgui/include/opencv2/highgui/highgui.hpp>
#include "/home/ec2-user/opencv-2.4.13/include/opencv/cv.h"
#include <fstream>
using namespace std;
using namespace cv;

CascadeClassifier haarcascade_frontalface_alt;

int main(int argc, char **argv)
{
    char *file_dir = argv[1];

    Mat pic = imread(file_dir, CV_LOAD_IMAGE_GRAYSCALE);
    
    const char *haarcascade_frontalface_alt_name = "./FaceData/haarcascade_frontalface_alt.xml";
    if( !haarcascade_frontalface_alt.load( haarcascade_frontalface_alt_name ) )
    { 
        cout << "ERROR: Could not load classifier haarcascade_frontalface_alt\n";
        exit(-1); 
    }
    vector<Rect> haarcascade_frontalface_alt_objs;
    haarcascade_frontalface_alt.detectMultiScale(pic, haarcascade_frontalface_alt_objs);

    Rect rect = haarcascade_frontalface_alt_objs[0];
    Mat roiImg = pic(rect);
    Mat resizedImg;
    resize(roiImg, resizedImg, Size(100,100), 0, 0, CV_INTER_LINEAR);
    equalizeHist(resizedImg, resizedImg);

    imwrite(file_dir, resizedImg);

    return 0;
}