<?php
	$uid = "";
	if ( isset($_POST["uid"]) ) { $cardUid = $_POST["uid"]; }
	$result = "<?php $" . "uid='" . $cardUid . "'; " . "echo $" . "uid;" . " ?>";
	file_put_contents("read-uid.php", $result);

