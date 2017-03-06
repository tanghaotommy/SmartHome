<?php

//require "deadline.php";
require "push.php";

// class MyThread extends Thread {

// 	var $mysqli;
// 	var $rid;
// 	var $id;
// 	var $time;

// 	public function __construct($mysqli, $rid, $id, $time)
// 	{
//  		$this->mysqli=$mysqli;
// 		$this->rid=$rid;
// 		$this->id=$id;
// 		$this->time=$time;
// 	}

// 	public function run() 
// 	{
//         OrderDeadline($this->mysqli, $this->rid, $this->id, $this->time);
//     }
// }

$json = file_get_contents('php://input');
$obj = json_decode($json);
$orderType = $obj->{'Type'};
$id = $obj->{'Id'};
$stat = -1;

$arr = array();

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
		$username = $row['username'];
		$result = $mysqli->query("SELECT * FROM Homes WHERE rid=(SELECT rid FROM RaspOwner WHERE uid='$uid')");
		if($result->num_rows != 0)
		{
			$row = $result->fetch_array();
			$rid = $row['rid'];
			$homename = $row['homename'];

			if($orderType == 'OpenDoor')
			{
				$type = 1;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'TurnOnLight') 
			{
				$type = 2;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'TurnOffLight') 
			{
				$type = 3;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'HomeStatus') 
			{
				$type = 4;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'ViewPhoto') 
			{
				$type = 5;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '', '$time')");

				//$time = time();
				//$t = new MyThread($mysqli, $rid, $id, $time);
				//$t->start();

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg['Id'] = $id;
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'ViewVideo') 
			{
				$type = 6;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'SendAlert') 
			{
				$type = 7;
				//$result = $mysqli->query("INSERT INTO Notifications VALUES ('$rid', '$type', '')");

				$msg = array();
				$msg['Type'] = $orderType;
				$msg['Content'] = "";
				$msg_json = json_encode($msg);
				post_pi($homename, $msg_json);
			}
			elseif ($orderType == 'AddFace')
			{
				$type = 8;

				$bufferType = 1;
				$result = $mysqli->query("SELECT * FROM Buffer WHERE uid='$uid' AND type='$bufferType'");
				$row = $result->fetch_array();
				$oriPath = $row['content'];
				exec("./facerecognition $oriPath",$result,$succ);
				if($succ == 0)
				{
					if (!file_exists("FaceData/trainingdata/$username"))
						mkdir ("FaceData/trainingdata/$homename");
					$time = time();
					$desPath = "FaceData/trainingdata/$username/$time.jpg";
					copy($oriPath, $desPath);
					$facePath = './'.$desPath;
					$mysqli->query("INSERT INTO Faces VALUES ('$uid', '$facePath')");
					$mysqli->query("DELETE FROM Buffer WHERE uid='$uid' AND type='$bufferType'");
				}
				else
				{
					$status = 13;
					// echo "Execution error";
				}
			}

			$stat = 0;
			//echo "Add the order successfully";
		}
		else 
		{
			$stat = 9;
			//echo "No such owner in database!";
		}      
    }
}

$arr["Status"] = $stat;
echo json_encode($arr);

?>
