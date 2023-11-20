<?php
// Logout dosen
session_start();

session_destroy();
session_unset();
$_SESSION = [];

setcookie('lecturer', '', time()-(3600*4)); // hapus cookie dosen 4 jam ke belakang

header("Location: login.php");
exit;