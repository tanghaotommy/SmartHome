<?php
$json = file_get_contents('php://input');
$obj = json_decode($json);
$id = $obj->{'Id'};
$stat = -1;
$response = array();

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
		$stat = 1;
		//echo "Cannot access the database!";
	    die('Could not connect: ' . mysqli_connect_error()); 
	}
	$result = $mysqli->query("SELECT * FROM Users WHERE fid='$id'");
	if($result->num_rows == 0)
	{
		$result = $mysqli->query("INSERT INTO Users VALUES ('', '', '', '$id')");
		$stat = 0;
		//echo "Register successfully";
	}
	else
	{
		$stat = 2;
		//echo "Wrong Facebook ID!";
	}
    
}

$arr["Status"] = $stat;
echo json_encode($arr);


?>