<?php
require_once 'DBConnection.php'; // Include file DatabaseConnection.php

class Authentication {
  private $nim;
  private $password;
  private $conn; // Objek koneksi database

  public function __construct($nim, $password) {
    $this->nim = $nim;
    $this->password = $password;

    // Membuat objek koneksi database saat objek Authentication dibuat
    $config = parse_ini_file('.env');
    $this->conn = new DatabaseConnection($config["DB_HOST"], $config["DB_NAME"], $config["DB_USER"], $config["DB_PASS"]);
  }

  public function login() : ?array {
    // Mendapatkan objek koneksi database dari DatabaseConnection
    $databaseConn = $this->conn->getConnection();

    // Buat query SQL untuk memeriksa username
    $query = "SELECT * FROM tbl_mhsw WHERE nim = :nim";
    $stmt = $databaseConn->prepare($query);
    $stmt->bindParam(':nim', $this->nim);
    $stmt->execute();

    if ($stmt->rowCount() > 0) {
      // Username ditemukan
      $user = $stmt->fetch(PDO::FETCH_ASSOC);

      // Periksa apakah password cocok
      if (password_verify($this->password, $user['password'])) {
        // Password cocok, pengguna berhasil login
        return $user;
      }
    }
    return null; // Username tidak ditemukan atau password tidak cocok
  }
}