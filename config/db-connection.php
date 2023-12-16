<?php
// koneksi dengan database MariaDB: ver-10.4.28
class DbConnection {
  private $db_host, $db_name, $db_user, $db_pass, $pdo;

  public function __construct($db_host, $db_name, $db_user, $db_pass) {
    $this->db_host = $db_host;
    $this->db_name = $db_name;
    $this->db_user = $db_user;
    $this->db_pass = $db_pass;
  }

  private function db_connect() {
    try {
      $dsn = "mysql:host=" . $this->db_host . ";dbname=" . $this->db_name;
      $this->pdo = new PDO($dsn, $this->db_user, $this->db_pass);
      $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch(PDOException $e) {
      die("Problem with database connection!: " . $e->getMessage());
    }
  }

  public function get_db_connection() {
    $this->db_connect();
    return $this->pdo;
  }
}