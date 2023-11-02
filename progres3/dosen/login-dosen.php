<?php
session_start();

require "../cookie.php";

if ( isset($_COOKIE["dosen"]) ) {
  $hashedCookieDosen = $_COOKIE["dosen"];

  $result = new Cookie();
  $hashedValue = $result->setCookieDosen($dosen["nama"]);

  if ($hashedCookieDosen === $hashedValue) {
    $_SESSION["dosen"] = $dosen;
  }
}

if ( isset($_SESSION["dosen"]) ) {
  header("Location: dashboard-dosen.php");
  exit;
}

require "../autentikasi.php";

if ( isset($_POST["login"]) ) {
  if ( isset($_POST["nip"]) && isset($_POST["password"]) ) {
    $nip = htmlspecialchars($_POST["nip"], ENT_QUOTES);
    $password = htmlspecialchars($_POST["password"], ENT_QUOTES);

    $login = new Authentication($nip, $password);
    $dosen = $login->getDosenLogin();

    if ( $dosen ) {
      $_SESSION["dosen"] = $dosen;

      if ( isset($_POST["remember"]) ) {
        setcookie("dosen", hash("sha256", $dosen["nama"]), time()+(2*3600));
      }

      header("Location: dashboard-dosen.php");
      exit;
    }
    else {
      echo "<script>alert('Login gagal');</script>";
    }
  }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login Page Dosen</title>
</head>
<body>
  <form action="" method="POST">
    <label for="nip">NIP: </label>
    <input type="text" name="nip" id="nip" placeholder="Your NIP" size="20" autofocus autocomplete="off"><br>

    <label for="password">Password: </label>
    <input type="password" name="password" id="password" placeholder="Your Password" size="20" autocomplete="off"><br>

    <input type="checkbox" id="remember" name="remember">
    <label for="remember">Remember me</label><br>

    <button type="submit" name="login">Login</button>
  </form>
  <br>
  <a href="../mahasiswa/login-mahasiswa.php">Login Mahasiswa</a>
</body>
</html>