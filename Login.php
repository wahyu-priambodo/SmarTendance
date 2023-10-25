<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login Page</title>
</head>
<body>
  <form action="Login.php" method="POST">
    <label for="NIM">NIM: </label>
    <input id="NIM" type="text" name="NIM" placeholder="NIM"><br>
    <label for="Password">Password: </label>
    <input id="Password" type="password" name="Password" placeholder="Password"><br>
    <button type="submit">Login</button>
  </form>
</body>
</html>

<?php
require_once 'Authentication.php'; // Include file Autentikasi.php

// Cek form menggunakan metode POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if (isset($_POST['NIM']) && isset($_POST['Password'])) {
    $username = htmlspecialchars($_POST['NIM'], ENT_QUOTES);
    $password = htmlspecialchars($_POST['Password'], ENT_QUOTES);

    $autentikasi = new Authentication($username, $password);

    if ($autentikasi->login()) {
      $user = $autentikasi->login();
      echo "Login berhasil. Selamat datang, " . $user['nama'] . "!";

      header("Location: dashboard.php"); // Redirect ke halaman dashboard
      exit; // Keluar untuk menghentikan eksekusi selanjutnya
    } else {
      echo "Gagal login. Periksa username dan kata sandi.";
    }
  } else {
    echo "Username dan kata sandi harus diisi.";
  }
}