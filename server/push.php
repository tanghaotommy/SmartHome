<?php

$serverIP = "http://54.183.198.179/";

function post_mobile($id, $type, $content)
{
	$ch = curl_init();

	$accesstoken = "EAAXGIRjqT70BACN38jI4IH6CgJYAaUBR5uQnelCUdiOXnifHuuTb1m7CQ986JpZA21ZAaLPNzaRGT8YgvBZBeM6nposWzPY1La5KKx4g1kvB6pQEIcQj6ndnvrJqIyCrFZBT6la6ZBHopq7yrfxZBB8Hef0XYiRcov3LE93ecn3AZDZD";
	curl_setopt($ch, CURLOPT_URL, "https://graph.facebook.com/v2.6/me/messages?access_token=$accesstoken");
	curl_setopt($ch, CURLOPT_HEADER, True);
	curl_setopt($ch, CURLOPT_POST, True);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

	$body = array();
	$body['recipient']['id'] = "$id";
	if($type == "Text")
	{
		$body['message']['text'] = $content;
	}
	elseif ($type == "Image") 
	{
		$body['message']['attachment']['type'] = 'image';
		$body['message']['attachment']['payload']['url'] = $content;
	}
	elseif ($type == "Video") 
	{
		$body['message']['attachment']['type'] = 'video';
		$body['message']['attachment']['payload']['url'] = $content;
	}	
	$json = json_encode($body);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $json);

	$result = curl_exec($ch);

	curl_close($ch);
}

function post_pi($homename, $content)
{
	exec("mosquitto_pub -h localhost -t /home/$homename -m '$content'");
}

?> 
