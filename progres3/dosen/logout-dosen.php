<?php
// Logout dosen
session_start();

session_destroy();
session_unset();
$_SESSION = [];

setcookie("dosen", "", time()-(4*3600)); // hapus cookie dosen 4 jam ke belakang

header("Location: login-dosen.php");
exit;