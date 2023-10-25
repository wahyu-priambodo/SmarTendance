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
      header("Location: ../frontend/index.html?username=" . $user["nama"] . "&nim=" . $user["nim"] . "&age=" . $user["usia"]); // Redirect ke halaman dashboard Mahasiswa
      exit; // Keluar untuk menghentikan eksekusi selanjutnya
    } else {
      header("Location: ../frontend/Login_mhsw.html?error=NIM atau password Anda salah!");
    }
  } else {
    echo "Username dan kata sandi harus diisi.";
  }
}