<?php
require 'push.php';

$json = file_get_contents('php://input');
$obj = json_decode($json);
$homename = $obj->{'Homename'};
$image = $obj->{'Image'};
$raw = $obj->{'Raw'};
$status = -1;

if($homename == "")
{
    $status = 7;
    //echo "Home name cannot be empty!";
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
	$query = $mysqli->query("SELECT * FROM Homes WHERE homename='$homename'");
    if($query->num_rows==0)
    {
		$status = 6;
		//echo "Wrong homename!";
	}
	else 
	{
		$imageData = base64_decode($image);
		//$imageDecompressed = gzdecode($imageData);
		$rawData = base64_decode($raw);
		$time = time();
		$faceFile_dir="UploadedFaceImages/$homename/$time.jpg";
		$rawFile_dir="UploadedFaceImages/$homename/$time.1.jpg";
		if (!file_exists("UploadedFaceImages/$homename"))
			mkdir ("UploadedFaceImages/$homename");
		if($fp = fopen($faceFile_dir,'w'))
		{
			if(fwrite($fp,$imageData))
				fclose($fp);
		}
		if($fp = fopen($rawFile_dir,'w'))
		{
			if(fwrite($fp,$rawData))
				fclose($fp);
		}
	
		$row = $query->fetch_array();
		$rid = $row['rid'];
		exec("./facerecognition $faceFile_dir $rid",$result,$succ);
		if($succ == 0)
		{
			$query = $mysqli->query("SELECT * FROM Users WHERE uid='$result[0]'");
			if($query->num_rows==0)
			{
				$status = 8;
				//echo "No such user in face database!";
				$query = $mysqli->query("SELECT fid FROM Users WHERE EXISTS (SELECT uid FROM RaspOwner WHERE Users.uid=RaspOwner.uid AND rid=(SELECT rid FROM Homes WHERE homename='$homename'))");
				if($query->num_rows==0)
				{
					$status = 9;
					//echo "Cannot find owner to notify!";
				}
				else 
				{
					while ($row = $query->fetch_assoc())
					{
						$fid = $row['fid'];
						post_mobile($fid, "Text", "There is someone I don't know who he/she is");
						post_mobile($fid, "Image", $serverIP.$rawFile_dir);
					}
					$status = 0;
					//echo "Send the stranger notification to home owner successfully.";
				}

			}
			else
			{
				$row = $query->fetch_array();
				$username = $row['username'];
				$query = $mysqli->query("SELECT rid FROM RaspOwner WHERE uid='$result[0]'");
				if($query->num_rows==0)
				{
					$rid = -1; // The raspberryPi that user has
				}
				else 
				{
					$row = $query->fetch_array();
					$rid = $row['rid']; // The raspberryPi that user has
				}
				$query = $mysqli->query("SELECT rid FROM Homes WHERE homename='$homename'");
				if($query->num_rows==0)
				{
					$status = 6;
					//echo "Wrong homename!";
				}
				else 
				{
					$row = $query->fetch_array();
					$homeid = $row['rid']; // The raspberryPi that controls the camera
					if($homeid == $rid)
					{
						$msg = array();
						$msg['Type'] = 'OpenDoor';
						$msg['Content'] = "";
						$msg_json = json_encode($msg);
						post_pi($homename, $msg_json);
						$status = 0;
						//echo "Open the door!";
					}
					else 
					{
						$query = $mysqli->query("SELECT fid FROM Users WHERE EXISTS (SELECT uid FROM RaspOwner WHERE Users.uid=RaspOwner.uid AND rid=(SELECT rid FROM Homes WHERE homename='$homename'))");
						if($query->num_rows==0)
						{
							$status = 9;
							//echo "Cannot find owner to notify!";
						}
						else 
						{
							while ($row = $query->fetch_assoc())
							{
								$fid = $row['fid'];
								post_mobile($fid, "Text", "$username is at the front of your door!");
								post_mobile($fid, "Image", $serverIP.$rawFile_dir);
							}
							$status = 0;
							//echo "Send the friend notification to home owner successfully.";
						}
					}
				}

			}       
		}     
		else
		{
			$status = 13;
			// echo "Execution error"; 
		}
	}
    
}

$recognition['Status'] = $status;
echo json_encode($recognition);
?>
