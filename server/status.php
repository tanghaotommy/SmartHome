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
		$stat = 2;
		//echo "No such user id!";
	}
	else
	{
        $row = $result->fetch_array();
        $uid = $row['uid'];
		$result = $mysqli->query("SELECT * FROM RaspOwner WHERE uid='$uid'");
		$row = $result->fetch_array();
		$rid = $row['rid'];
		//$result = $mysqli->query("SELECT * FROM Status WHERE rid='$rid'");
		//$row = $result->fetch_array();
		//$content = $row['content'];

		$response['Content'] = "Content";
		$stat = 0;
	}
}

$response['Status'] = $stat;
echo json_encode($response);

?>