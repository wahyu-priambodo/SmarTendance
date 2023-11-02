<?php
session_start();

require "../cookie.php";

if ( isset($_COOKIE["mhsw"]) ) {
  $hashedCookieMhsw = $_COOKIE["mhsw"];

  $result = new Cookie();
  $hashedValue = $result->setCookieMhsw($mhsw["nama"]);

  if ($hashedCookieMhsw === $hashedValue) {
    $_SESSION["mhsw"] = $mhsw;
  }
}

if ( isset($_SESSION["mhsw"]) ) {
  header("Location: dashboard-mahasiswa.php");
  exit;
}

require "../autentikasi.php";

if ( isset($_POST["login"]) ) {
  if ( isset($_POST["nim"]) && isset($_POST["password"]) ) {
    $nim = htmlspecialchars($_POST["nim"], ENT_QUOTES);
    $password = htmlspecialchars($_POST["password"], ENT_QUOTES);

    $login = new Authentication($nim, $password);
    $mhsw = $login->getMahasiswaLogin();

    if ( $mhsw ) {
      $_SESSION["mhsw"] = $mhsw;

      if ( isset($_POST["remember"]) ) {
        setcookie("mhsw", hash("sha256", $mhsw["nama"]), time()+(2*3600)); // masa berlaku cookie mahasiswa selama 2 jam
      }

      header("Location: dashboard-mahasiswa.php");
      exit;
    }
    else {
      echo "<script>alert('Login gagal');</script>";
    }
  }
}
?>

<?php if ( !isset($_SESSION["mhsw"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login Page Mahasiswa</title>
</head>
<body>
  <form action="" method="POST">
    <label for="nim">NIM: </label>
    <input type="text" name="nim" id="nim" placeholder="Your NIM" size="20" autofocus autocomplete="off"><br>
    
    <label for="password">Password: </label>
    <input type="password" name="password" id="password" placeholder="Your Password" size="20" autocomplete="off"><br>
    
    <input type="checkbox" id="remember" name="remember">
    <label for="remember">Remember me</label><br>
    
    <button type="submit" name="login">Login</button>
  </form>
  <br>
  <a href="../dosen/login-dosen.php">Login Dosen</a>
</body>
</html>
<?php endif; ?>