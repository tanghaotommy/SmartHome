<?php
$json = file_get_contents('php://input');
$obj = json_decode($json);
$username = $obj->{'Username'};
$stat = -1;

if($username == "")
{
	$stat = 5;
	//echo "User name cannot be empty!";
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
    $result = $mysqli->query("SELECT * FROM Users WHERE username='$username'");
	if($result->num_rows == 0)
	{
		$stat = 4;
		//echo "No such user username!";
	}
	else
	{
        $row = $result->fetch_array();
        $uid = $row['uid'];
        $result = $mysqli->query("SELECT * FROM Notifications WHERE uid='$uid'");
        $type = -1;
        $arr = array();
        if($result->num_rows == 0)
        {
            $stat = 11;
            // echo "No new notification"
            $arr['Status'] = $stat;
        }
        else
        {
            $stat = 10;
            // echo "Found new notifications"
            $index = 1;
            $arr['Status'] = $stat;
            while ($row = $result->fetch_assoc())
            {
                $temp = array();
                $temp['Type'] = $row['type'];
                $temp['Content'] = json_decode($row['content']);
                $arr[$index] = $temp;
		        $index++;
            }
            $mysqli->query("DELETE FROM Notifications WHERE uid='$uid'");
        }
    }
}

if($stat == 10) 
    echo stripslashes(json_encode($arr));
else
{
	$arr = array("Status" => $stat);
	echo json_encode($arr);
}

?>
