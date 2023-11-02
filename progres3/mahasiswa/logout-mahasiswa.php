<?php
// Logout mahasiswa
session_start();

session_destroy();
session_unset();
$_SESSION = [];

setcookie("mhsw", "", time()-(4*3600)); // hapus cookie mahasiswa 4 jam ke belakang

header("Location: login-mahasiswa.php");
exit;