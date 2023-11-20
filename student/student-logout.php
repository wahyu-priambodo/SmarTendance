<?php
// Logout mahasiswa
session_start();

session_destroy();
session_unset();
$_SESSION = [];

setcookie('student', '', time()-(3600*4)); // hapus cookie mahasiswa 4 jam ke belakang

header('Location: ../index.php');
exit;