<?php
session_start();
header('Content-type: application/json');

$json = file_get_contents('php://input');
$obj = json_decode($json);
$username = $obj->{'Username'};
$password = $obj->{'Password'};
$stat = -1;

if($username == "")
{
	$stat = 5;
	//echo "Username cannot be empty!";
}
elseif($password == "")
{
	$stat = 1;
	//echo "User password cannot be empty!";
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
	$result = $mysqli->query("SELECT * FROM Users WHERE username='".$username."'");
	if($result->num_rows==0)
	{
		$stat = 4;
		//echo "No such username!";
	}
	else
	{
		$row = $result->fetch_array();
		if($row['password']==$password)
		{
			$_SESSION['USER_ID']   =   $row['uid'];
        	$_SESSION['USERNAME']  =   $row['username'];
			$stat = 0;
			//echo "Login successfully!";
		}
		else
		{
			$stat = 4;
			//echo "Wrong password!";
		}
	}
}
$login = array('Status' => $stat);
echo json_encode($login);
?>
