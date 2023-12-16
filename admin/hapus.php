<?php
// Halaman hapus data mahasiswa
session_start();

if ( !isset($_COOKIE["admin"]) || $_COOKIE["admin"] !== hash("sha256", $_SESSION["admin"]["nama"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("admin", "", time()-14400); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login-admin.php");
  exit;
}

if ( !isset($_SESSION["admin"]) ) {
  header("Location: dashboard-admin.php");
  exit;
}

require "../fungsi.php";
$admin = new Action();

// mengambil parameter nim dari dashboard-admin.php
if ( isset($_GET["nim"]) ) {
  $nimMhsw = $_GET["nim"];
  $admin->deleteDataMhsw($nimMhsw);
  header("Location: dashboard-admin.php?message=Data mahasiswa berhasil terhapus");
  exit;
}
else {
  header("Location: dashboard-admin.php?message=NIM tidak dikenal!");
  exit;
}

