<?php
require 'push.php';

$json = file_get_contents('php://input');
$obj = json_decode($json);
$homename = $obj->{'Homename'};
$id = $obj->{'Id'};
$type = $obj->{'Type'};
$message = $obj->{'Message'};
$stat = -1;

if($homename == "")
{
    $stat = 7;
    //echo "Homename cannot be empty!";
}
else
{
    if($type == "OpenDoor")
    {
        $mysqli = new mysqli("newdatabase.cii5tvbuf3ji.us-west-1.rds.amazonaws.com","root","password","SmartHome");
        if (mysqli_connect_errno())
        {
            $stat = 1;
            //echo "Cannot access the database!";
            die('Could not connect: ' . mysqli_connect_error()); 
        }
        $result = $mysqli->query("SELECT fid FROM Users WHERE uid IN (SELECT uid FROM RaspOwner WHERE rid IN (SELECT rid FROM RaspOwner WHERE uid = (SELECT uid FROM Users WHERE fid = $id)))");
        while ($row = $result->fetch_assoc())
        {
            $fid = $row['fid'];
			post_mobile($fid, "Text", $message);
        }
        $stat = 0;
    }
    else
    {
        post_mobile($id, "Text", $message);
        $stat = 0;
    }
}

$arr = array("Status" => $stat);
echo json_encode($arr);

?>
