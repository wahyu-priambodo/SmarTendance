<?php
// Dashboard dosen
session_start();

if ( isset($_COOKIE["dosen"]) && $_COOKIE["dosen"] !== hash("sha256", $_SESSION["dosen"]["nama"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("dosen", "", time()-(4*3600)); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login-dosen.php");
  exit;
}

if ( !isset($_SESSION["dosen"]) ) {
  header("Location: login-dosen.php");
  exit;
}

?>

<?php if ( isset($_SESSION["dosen"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Dosen</title>
</head>
<body>
  <h1>Selamat datang, <?= $_SESSION["dosen"]["nama"]; ?></h1>
  <a href="logout-dosen.php">Logout</a>
</body>
</html>
<?php endif; ?>