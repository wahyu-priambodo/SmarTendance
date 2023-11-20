<?php
// Logout admin
session_start();

session_destroy();
session_unset();
$_SESSION = [];

setcookie('admin', '', time()-(3600*4)); // hapus cookie admin 4 jam ke belakang

header('Location: login.php');
exit;