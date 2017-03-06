<?php

$json = file_get_contents('php://input');
$obj = json_decode($json);
$type = $obj->{'type'};
$id = $obj->{'id'};
$url = $obj->{'url'};
$stat = -1;

if($id == "")
{
    $stat = 3;
    //echo "User id cannot be empty!";
}
else 
{
	$mysqli = new mysqli("newdatabase.cii5tvbuf3ji.us-west-1.rds.amazonaws.com","root","password","SmartHome");
    if (mysqli_connect_errno())
    {
        $status = 1;
        //echo "Cannot access the database!";
        die('Could not connect: ' . mysqli_connect_error()); 
    }
    $result = $mysqli->query("SELECT * FROM Users WHERE fid='$id'");
	if($result->num_rows == 0)
    {
        $stat = 2;
        //echo "No such user id! (Wrong Facebook ID)";
    }
	else 
	{
		$row = $result->fetch_array();
		$username = $row['username'];
		$uid = $row['uid'];
		$image = file_get_contents($url);
		$time = time();
		$path = "./FaceData/trainingdata/$username/$time.jpg";
		file_put_contents($path, $image);
		$result = $mysqli->query("INSERT INTO Faces VALUES ($uid,$path)");
		$stat = 0;
		//echo "Add new face image into database successfully";
	}
}

$arr = array("Status" => $stat);
echo json_encode($arr);

?>
