<?php
// file kumpulan method/function untuk operasi CRUDS
require "koneksi.php";

class Action {
  private $conn;

  public function __construct() {
    $this->conn = $GLOBALS["databaseConn"];
  }

  // fungsi menampilkan semua data mahasiswa
  public function readDataMhsw() {
    $query = "SELECT `nim`, `nama`, `uid`, `kelas` FROM tbl_mhsw ORDER BY `nim` ASC";
    $stmt = $this->conn->query($query);
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return $result;
  }
  
  // fungsi tambah data mahasiswa
  public function createDataMhsw($nimMhsw, $passMhsw, $uidMhsw, $namaMhsw, $kelasMhsw, $noTelpMhsw) {
    $hashedPassword = password_hash($passMhsw, PASSWORD_DEFAULT);
    
    $query = "INSERT INTO tbl_mhsw (`nim`, `password`, `uid`, `nama`, `kelas`, `no_telp`) VALUES (:nim, :pass, :uid, :nama, :kelas, NULLIF(:no_telp, ''))";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nimMhsw, PDO::PARAM_STR);
    $stmt->bindParam(":pass", $hashedPassword, PDO::PARAM_STR);
    $stmt->bindParam(":uid", $uidMhsw, PDO::PARAM_STR);
    $stmt->bindParam(":nama", $namaMhsw, PDO::PARAM_STR);
    $stmt->bindParam(":kelas", $kelasMhsw, PDO::PARAM_STR);
    
    // Menangani no_telp secara terpisah jika menggunakan NULLIF di dalam query
    if ( empty($noTelpMhsw) ) {
      $stmt->bindValue(':no_telp', null, PDO::PARAM_NULL);
    }
    else {
      $stmt->bindParam(":no_telp", $noTelpMhsw, PDO::PARAM_STR);
    }

    $result = $stmt->execute();
    return $result;
  }

  // fungsi update data mahasiswa
  public function updateDataMhsw($namaBaru, $uidBaru, $nimMhsw) {
    $query = "UPDATE tbl_mhsw SET `nama` = :nama, `uid` = :uid WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nama", $namaBaru, PDO::PARAM_STR);
    $stmt->bindParam(":uid", $uidBaru, PDO::PARAM_STR);
    $stmt->bindParam(":nim", $nimMhsw, PDO::PARAM_STR);

    $result = $stmt->execute();
    if ( !$result ) {
        $error = $stmt->errorInfo();
        echo "Error: " . $error[2]; // Menampilkan pesan kesalahan
    }

    return $result;
  }

  // fungsi hapus data mahasiswa
  public function deleteDataMhsw($nimMhsw) {
    $query = "DELETE FROM tbl_mhsw WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nimMhsw, PDO::PARAM_STR);
    
    $result = $stmt->execute();
    return $result;
  }

  // fungsi cari data mahasiswa
  public function cariDataMhsw($keyword) {
    $keyword = "%$keyword%";

    $query = "SELECT * FROM tbl_mhsw WHERE `nim` LIKE :keyword OR `nama` LIKE :keyword OR `kelas` LIKE :keyword";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":keyword", $keyword, PDO::PARAM_STR);

    $result = $stmt->execute();
    if ( !$result ) {
      $error = $stmt->errorInfo();
      echo "Error: " . $error[2]; // Menampilkan pesan kesalahan
      return []; // Return array kosong jika terjadi kesalahan
    }

    $data = $stmt->fetchAll(PDO::FETCH_ASSOC); // Mengambil hasil pencarian
    return $data;
  }

  // fungsi untuk mencari nama mahasiswa berdasarkan nim
  public function getInfoByNim($nimMhsw) {
    $query = "SELECT `nama` FROM tbl_mhsw WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nimMhsw, PDO::PARAM_STR);
    $stmt->execute();
    
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return $result;
  }
}