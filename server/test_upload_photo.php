<?php

$image = file_get_contents('php://input');
$time = time();
$file_dir = "UploadedFaceImages/$time.jpg";
$username = 'ggg';

if($fp = fopen($file_dir,'w'))
{
	if(fwrite($fp,$image))
		fclose($fp);
}

$imageCompressed = gzencode($image);
$imageString = base64_encode($imageCompressed);
$type = 1;
$arr = array();
//$arr['Name'] = $username;
//$arr['Image'] = $imageString;
//$content = json_encode($arr);
//echo $content;

$mysqli = new mysqli("newdatabase.cii5tvbuf3ji.us-west-1.rds.amazonaws.com","root","password","SmartHome");
if (mysqli_connect_errno())
{
	$stat = 3;
	//echo "Cannot access the database!";
	die('Could not connect: ' . mysqli_connect_error());
}
$result = $mysqli->query("SELECT * FROM Users WHERE username='$username'");
if($result->num_rows == 0)
{
	$stat = 2;
	//echo "No such user username!";
}
else
{
	$stat = 0;
	$row = $result->fetch_array();
	$uid = $row['uid'];
	$result = $mysqli->query("INSERT INTO Notifications VALUES ('$uid', '$type', '$content')");
}

$arr['Status'] = $stat;
$content = json_encode($arr);
echo $content;

?>