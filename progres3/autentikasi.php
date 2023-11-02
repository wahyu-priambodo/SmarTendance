<?php
// file untuk user melakukan autentikasi (login)
require_once 'koneksi.php';

class Authentication {
  private $id, $password, $conn;

  public function __construct($id, $password) {
    $this->id = $id;
    $this->password = $password;
    $this->conn = $GLOBALS['databaseConn'];
  }

  private function loginAdmin() : ?array {
    $query = "SELECT * FROM tbl_admin WHERE id_admin = :id_admin";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':id_admin', $this->id);
    $stmt->execute();

    $admin = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($admin) {
      if (password_verify($this->password, $admin['password'])) {
        return $admin;
      }
    }
    return null;
  }

  private function loginDosen() : ?array {
    $query = "SELECT * FROM tbl_dosen WHERE nip = :nip";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':nip', $this->id);
    $stmt->execute();

    $dosen = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($dosen) {
      if (password_verify($this->password, $dosen['password'])) {
        return $dosen;
      }
    }
    return null;
  }
  
  private function loginMahasiswa() : ?array {
    $query = "SELECT * FROM tbl_mhsw WHERE nim = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':nim', $this->id);
    $stmt->execute();

    $mhsw = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($mhsw) {
      if (password_verify($this->password, $mhsw['password'])) {
        return $mhsw;
      }
    }
    return null;
  }

  public function getAdminLogin() {
    return $this->loginAdmin();
  }

  // Fungsi getter untuk loginDosen
  public function getDosenLogin() {
    return $this->loginDosen();
  }

  // Fungsi getter untuk loginMahasiswa
  public function getMahasiswaLogin() {
    return $this->loginMahasiswa();
  }
}