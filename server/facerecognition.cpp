#include </home/ec2-user/opencv-2.4.13/modules/contrib/include/opencv2/contrib/contrib.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/core/include/opencv2/core/core.hpp>
#include </home/ec2-user/opencv-2.4.13/modules/highgui/include/opencv2/highgui/highgui.hpp>
#include "/home/ec2-user/opencv-2.4.13/include/opencv/cv.h"
#include <fstream>
#include <mysql.h>
#include <cstdlib>
#include <sstream>
using namespace std;
using namespace cv;

Ptr<cv::FaceRecognizer> model = createLBPHFaceRecognizer();
vector<Mat> images;
vector<int> labels;

int LoadDatabase(int rid)
{
    MYSQL conn;
    MYSQL_RES *res_ptr;
    MYSQL_FIELD *field;
    MYSQL_ROW result_row;
    int row, column;
    int i, j;
    mysql_init(&conn);
    if (mysql_real_connect(&conn, "newdatabase.cii5tvbuf3ji.us-west-1.rds.amazonaws.com", "root", "password", "SmartHome", 0, NULL, CLIENT_FOUND_ROWS))
    {
		char* queryStr = new char[200];
		sprintf(queryStr, "SELECT * FROM Faces WHERE EXISTS (SELECT * FROM RaspOwner WHERE rid=\'%d\' AND Faces.uid=RaspOwner.uid) OR uid in (SELECT uid FROM Friends WHERE rid=\'%d\' AND Faces.uid=Friends.uid)", rid, rid);
		int res = mysql_query(&conn, queryStr);
		delete[] queryStr;
		if (res)
		{
			mysql_close(&conn);
			cout << "Query fail" << endl;
			return -1;
		}
		res_ptr = mysql_store_result(&conn);
		if (res_ptr)
		{
			row = mysql_num_rows(res_ptr) + 1;
			for (i = 1; i < row; i++)
			{
				result_row = mysql_fetch_row(res_ptr);
				labels.push_back(atoi(result_row[0]));
				images.push_back(imread(result_row[1], 0));
			}
		}
		else
		{
			cout << "Store fail" << endl;
			return -1;
		}
        mysql_close(&conn);
    }
    else
    {
        cout<<"Connect fail"<<endl;
        fprintf(stderr, "error: %s",mysql_error(&conn)); 
        return -1;
    }
    return 0;
}

int recognize(IplImage *img)
{
    int id = -1;
    int predictedLabel = -1;
    Mat test = img;
    double predicted_confidence = 0.0;
    model->set("threshold", 20.0);
    model->predict(test, predictedLabel, predicted_confidence);
    id = predictedLabel;
    return id;
}

int main(int argc, char **argv)
{
    char *file_dir = argv[1];
	int rid = atoi(argv[2]);
    int result = LoadDatabase(rid);
    if (result == -1)
    {
        cout << "Cannot load database" << endl;
        return -1;
    }
    if (images.size() <= 2)
    {
        cout << "This demo needs at least 2 images to work." << endl;
        return -1;
    }
    model->train(images, labels);
    IplImage *frame, *frame_copy = 0;
    frame = cvLoadImage(file_dir, CV_LOAD_IMAGE_ANYDEPTH);
    if (!frame)
    {
        cout << "Cannot load the image" << endl;
        return -1;
    }
    frame_copy = cvCreateImage(cvSize(100, 100), IPL_DEPTH_8U, frame->nChannels);
    if (frame->origin == IPL_ORIGIN_TL)
        cvCopy(frame, frame_copy, 0);
    else
        cvFlip(frame, frame_copy, 0);
    int id = recognize(frame_copy);
    cvReleaseImage(&frame);
    cvReleaseImage(&frame_copy);
    cout << id << endl;
    return 0;
}
