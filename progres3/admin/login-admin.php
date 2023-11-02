<?php
session_start();

require "../cookie.php";

if ( isset($_COOKIE["admin"]) ) {
  $hashedCookieAdmin = $_COOKIE["admin"];

  $result = new Cookie();
  $hashedValue = $result->setCookieAdmin($admin["nama"]);

  if ($hashedCookieAdmin === $hashedValue) {
    $_SESSION["admin"] = $admin;
  }
}

if ( isset($_SESSION["admin"]) ) {
  header("Location: dashboard-admin.php");
  exit;
}

require "../autentikasi.php";

if ( isset($_POST["login"]) ) {
  if ( isset($_POST["id"]) && isset($_POST["password"]) ) {
    $id = htmlspecialchars($_POST["id"], ENT_QUOTES);
    $password = htmlspecialchars($_POST["password"], ENT_QUOTES);

    $login = new Authentication($id, $password);
    $admin = $login->getAdminLogin();

    if ( $admin ) {
      $_SESSION["admin"] = $admin;

      if ( isset($_POST["remember"]) ) {
        setcookie("admin", hash("sha256", $admin["nama"]), time()+(2*3600)); // masa berlaku cookie admin selama 2 jam
      }

      header("Location: dashboard-admin.php");
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
  <title>Login Page Admin</title>
</head>
<body>
  <form action="" method="POST">
    <label for="id">ID Admin: </label>
    <input type="text" name="id" id="id" placeholder="Your ID" size="20" autofocus autocomplete="off"><br>
    
    <label for="password">Password: </label>
    <input type="password" name="password" id="password" placeholder="Your Password" size="20" autofocus autocomplete="off"><br>
    
    <input type="checkbox" id="remember" name="remember">
    <label for="remember">Remember me</label><br>

    <button type="submit" name="login">Login</button>
  </form>
</body>
</html>