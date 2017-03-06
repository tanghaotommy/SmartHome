<?php

require "push.php";

function OrderDeadline($mysqli, $rid, $fid, $time)
{
	$interval = 5;
	sleep($interval);
	$result = $mysqli->query("SELECT * FROM Notifications WHERE rid='$rid' AND gentime='$time'");
	if($result->num_rows != 0)
	{
		post_mobile($fid, "Text", "Oh, I'm sorry. It seems that there is something wrong with the photo.");
	}
}

?> 