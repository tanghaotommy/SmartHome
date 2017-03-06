<?php
require 'push.php';

$json = file_get_contents('php://input');
$obj = json_decode($json);
$homename = $obj->{'Homename'};
$image = $obj->{'Image'};
$id = $obj->{'Id'};
$stat = -1;

if($homename == "")
{
    $stat = 7;
    //echo "Homename cannot be empty!";
}
else
{
    $imageData = base64_decode($image);
    //$imageDecompressed = gzdecode($imageData);
    $time = time();
    $file_dir="UploadedFaceImages/$homename/$time.jpg";
    if (!file_exists("UploadedFaceImages/$homename"))
        mkdir ("UploadedFaceImages/$homename");
    if($fp = fopen($file_dir,'w'))
    {
        if(fwrite($fp,$imageData))
        {
            fclose($fp); 
            // $mysqli = new mysqli("mysql.cii5tvbuf3ji.us-west-1.rds.amazonaws.com","root","password","SmartHome");
            // if (mysqli_connect_errno())
            // {
            //     $status = 1;
            //     //echo "Cannot access the database!";
            //     die('Could not connect: ' . mysqli_connect_error()); 
            // }
            // $result = $mysqli->query("SELECT fid FROM Users WHERE uid=(SELECT uid FROM RaspOwner WHERE rid=(SELECT rid FROM Homes WHERE homename='$homename'))");
            // if($result->num_rows == 0)
            // {
            //     $stat = 4;
            //     //echo "No such username!";
            // }
            // else
            // {
            //     $row = $result->fetch_array();
            //     $fid = $row['fid'];
		
            //     //post_mobile($fid, "Text", "Here is a photo shows the status outside your door.");
				
            // }

            post_mobile($id, "Image", $serverIP.$file_dir);
            $stat = 0;
            //echo "Push the notification successfully!";
        }
        else
        {
            $stat = 15;
            //echo "Cannot write the file!";
        }
    }
    else
    {
        $stat = 13;
        //echo "Cannot open the file!";
    }
}

$arr = array("Status" => $stat);
echo json_encode($arr);

?>
