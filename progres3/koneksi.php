<?php
// file untuk bisa konek dengan database MySQL/MariaDB
class Connection {
  private $dbHost, $dbName, $dbUser, $dbPass, $conn;

  public function __construct($dbHost, $dbName, $dbUser, $dbPass) {
    $this->dbHost = $dbHost;
    $this->dbName = $dbName;
    $this->dbUser = $dbUser;
    $this->dbPass = $dbPass;
    $this->connect();
  }

  private function connect() {
    try {
      $dsn = "mysql:host=" . $this->dbHost . ";dbname=" . $this->dbName;
      $this->conn = new PDO($dsn, $this->dbUser, $this->dbPass);
      $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch(PDOException $e) {
      die("Problem with database connection!: " . $e->getMessage());
    }
  }

  public function getConnection() {
    return $this->conn;
  }
}

$config = parse_ini_file('.env');
$database = new Connection($config['DB_HOST'], $config['DB_NAME'], $config['DB_USER'], $config['DB_PASS']);
$databaseConn = $database->getConnection();