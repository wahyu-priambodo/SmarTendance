<?php
// Dashboard dosen
session_start();

if ( isset($_COOKIE["lecturer"]) && $_COOKIE["lecturer"] !== hash("sha256", $_SESSION["lecturer"]["nama_dosen"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("lecturer", "", time()-(3600*4)); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login.php");
  exit;
}

if ( !isset($_SESSION["lecturer"]) ) {
  header("Location: login.php");
  exit;
}
?>

<?php if ( isset($_SESSION["lecturer"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard <?= $_SESSION['admin']['nama_admin'] ?></title>
</head>
<body>
  <h1>Selamat datang, <?= $_SESSION["lecturer"]["nama_dosen"]; ?></h1>
  <a href="lecturer-logout.php">Logout</a>
</body>
</html>
<?php endif; ?>