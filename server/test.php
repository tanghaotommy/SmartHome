<?php
require 'push.php';

$json = file_get_contents('php://input');
$obj = json_decode($json);
$image = $obj->{'Image'};
$rid = 1;

exec("./facerecognition $image $rid",$result,$succ);

if($succ == 0)
{
	echo $result;
}

?>