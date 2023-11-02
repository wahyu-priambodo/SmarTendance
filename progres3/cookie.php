<?php
// file untuk membuat cookie tiap user
require "koneksi.php";

class Cookie {
  private $conn;

  public function __construct() {
    $this->conn = $GLOBALS["databaseConn"];
  }

  public function setCookieAdmin($namaAdmin) {
    $query = "SELECT nama from tbl_admin WHERE nama = :nama";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nama", $namaAdmin);
    $stmt->execute();

    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return hash("sha256", $result); // hashed nama admin
  }

  public function setCookieDosen($namaDosen) {
    $query = "SELECT nama from tbl_dosen WHERE nama = :nama";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nama", $namaDosen);
    $stmt->execute();

    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return hash("sha256", $result); // hashed nama dosen
  }

  public function setCookieMhsw($namaMhsw) {
    $query = "SELECT nama from tbl_mhsw WHERE nama = :nama";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nama", $namaMhsw);
    $stmt->execute();

    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return hash("sha256", $result); // hashed nama mahasiswa
  }
}