<?php
// Dashboard mahasiswa
session_start();

if ( isset($_COOKIE["mhsw"]) && $_COOKIE["mhsw"] !== hash("sha256", $_SESSION["mhsw"]["nama"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("mhsw", "", time()-(4*3600)); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login-mahasiswa.php");
  exit;
}

if ( !isset($_SESSION["mhsw"]) ) {
  header("Location: login-mahasiswa.php");
  exit;
}

?>

<?php if ( isset($_SESSION["mhsw"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Mahasiswa</title>
</head>
<body>
  <h1>Selamat datang, <?= $_SESSION["mhsw"]["nama"]; ?></h1>
  <a href="logout-mahasiswa.php">Logout</a>
</body>
</html>
<?php endif; ?>