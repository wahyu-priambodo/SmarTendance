<?php declare(strict_types=1);

class DatabaseConnection {
  private $dbHost;
  private $dbName;
  private $dbUser;
  private $dbPass;
  private $conn;

  public function __construct($dbHost, $dbName, $dbUser, $dbPass) {
    $this->dbHost = $dbHost;
    $this->dbName = $dbName;
    $this->dbUser = $dbUser;
    $this->dbPass = $dbPass;
    $this->connect();
  }

  private function connect() {
    try {
      $dsn = "mysql:host=".$this->dbHost.";dbname=".$this->dbName;
      $this->conn = new PDO($dsn, $this->dbUser, $this->dbPass);
      $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch(PDOException $e) {
      die("Failed to connect to database $this->dbName: " . $e->getMessage());
    }
  }

  public function getConnection() {
    return $this->conn;
  }
}