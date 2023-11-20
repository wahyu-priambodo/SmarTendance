<?php declare(strict_types= 1);
setlocale(LC_TIME, 'id_ID');
date_default_timezone_set('Asia/Jakarta');

// file kumpulan method/function untuk operasi CRUDS
require_once __DIR__.'/../config/db-connection.php';

/* CLASS DbFunctions */
class DbFunctions extends DbConnection {
  private $conn;
  public function __construct($db_host, $db_name, $db_user, $db_pass) {
    parent::__construct($db_host, $db_name, $db_user, $db_pass);
    $this->conn = parent::get_db_connection();
  }

  /* -------- LOGIN FOR ADMIN, LECTURER, AND STUDENT -------- */
  // method untuk login admin
  private function login_admin($admin_id, $password) : ?array {
    $query = "SELECT * FROM tbl_admin WHERE `id_admin` = :id_admin";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':id_admin', $admin_id, PDO::PARAM_STR);
    $stmt->execute();

    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    if ( $row ) {
      $admin = $row;
      if (password_verify($password, $admin['password'])) {
        return $admin;
      }
    }
    return null;
  }

  // method untuk login dosen
  private function login_lecturer($nip, $password) : ?array {
    $query = "SELECT * FROM tbl_dosen WHERE `NIP` = :nip";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':nip', $nip, PDO::PARAM_STR);
    $stmt->execute();

    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    if ( $row ) {
      $dosen = $row;
      if (password_verify($password, $dosen['password'])) {
        return $dosen;
      }
    }
    return null;
  }

  // method untuk login mahasiswa/i
  private function login_student($nim, $password) : ?array {
    $query = "SELECT * FROM tbl_mhsw WHERE `NIM` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(':nim', $nim);
    $stmt->execute();

    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    if ( $row ) {
      $student = $row;
      if (password_verify($password, $student['password'])) {
        return $student;
      }
    }
    return null;
  }

  // fungsi getter untuk login admin
  public function get_admin_login($id_admin, $password) {
    return $this->login_admin($id_admin, $password);
  }

  // Fungsi getter untuk login dosen
  public function get_lecturer_login($nip, $password) {
    return $this->login_lecturer($nip, $password);
  }

  // Fungsi getter untuk login mahasiswa
  public function get_student_login($nim, $password) {
    return $this->login_student($nim, $password);
  }
  /* -------- LOGIN FOR ADMIN, LECTURER, AND STUDENT -------- */

  /* -------- CRUDS OPERATION -------- */
  // method untuk mendapatkan jumlah mahasiswa terdaftar (admin)
  public function get_total_students() {
    $query = "SELECT COUNT(*) FROM tbl_mhsw";
    $stmt = $this->conn->prepare($query);
    $stmt->execute();
    $total_students = $stmt->fetchColumn();
    return $total_students;
  }

  // method untuk mendapatkan jumlah dosen terdaftar (admin)
  public function get_total_lecturers() {
    $query = "SELECT COUNT(*) FROM tbl_dosen";
    $stmt = $this->conn->prepare($query);
    $stmt->execute();
    $total_students = $stmt->fetchColumn();
    return $total_students;
  }

  // method untuk mendapatkan jumlah course terdaftar (admin)
  public function get_total_courses() {
    $query = "SELECT COUNT(*) FROM tbl_course";
    $stmt = $this->conn->prepare($query);
    $stmt->execute();
    $total_students = $stmt->fetchColumn();
    return $total_students;
  }

  // method untuk mendapatkan jumlah kelas yang tersedia (admin)
  public function get_total_classes() {
    $query = "SELECT COUNT(*) FROM tbl_kelas";
    $stmt = $this->conn->prepare($query);
    $stmt->execute();
    $total_students = $stmt->fetchColumn();
    return $total_students;
  }

  // method untuk menampilkan semua data mahasiswa/i
  public function get_all_students_data() : ?array {
    $query = "SELECT `nama_mhsw`, `NIM`, `uid`, `kelas` FROM tbl_mhsw ORDER BY `NIM` ASC";
    $rows = $this->conn->query($query)->fetchAll(PDO::FETCH_ASSOC);

    if ( $rows ) {
      return $rows;
    }
    return null; // return null
  }

  // method untuk menampilkan semua data dosen
  public function get_all_lecturers_data() : ?array {
    $query = "SELECT tbl_dosen.`nama_dosen`, tbl_dosen.`NIP`, COUNT(tbl_course.`id_matkul`) AS jumlah_matkul, tbl_dosen.`prodi` FROM tbl_course INNER JOIN tbl_dosen ON tbl_dosen.`NIP` = tbl_course.`NIP` GROUP BY tbl_dosen.`NIP` ORDER BY tbl_dosen.`NIP` ASC";
    $rows = $this->conn->query($query)->fetchAll(PDO::FETCH_ASSOC);
    
    if ( $rows ) {
      return $rows;
    }
    return null;
  }

  // method untuk menampilkan semua course yang diikuti oleh mahasiswa/i
  public function get_all_student_courses($student_class) : ?array {
    $query = "SELECT tbl_course.`nama_matkul`, tbl_course.`id_matkul`, tbl_course.`hari`, tbl_course.`jam_mulai`, tbl_course.`jam_selesai`, tbl_course.`SKS`, tbl_dosen.`nama_dosen`
    FROM tbl_course
    INNER JOIN tbl_dosen
    ON tbl_course.`NIP` = tbl_dosen.`NIP`
    WHERE tbl_course.`kelas` = :kelas
    ORDER BY tbl_course.`hari`, tbl_course.`jam_mulai` ASC";

    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":kelas", $student_class, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    if ( $rows ) {
      return $rows;
    }
    return null;
  }

  // method untuk mengecek apakah course tersedia/tidak
  public function get_current_course($student_class, $current_day, $current_time) {
    $query = "SELECT `id_matkul`, `hari`, `jam_mulai`, `jam_selesai`
    FROM tbl_course
    WHERE `kelas` = :kelas AND `hari` = :hari
    ORDER BY `hari`, `jam_mulai` ASC";

    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":kelas", $student_class, PDO::PARAM_STR);
    $stmt->bindParam(":hari", $current_day, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $current_course = []; // untuk menyimpan id_matkul yang tersedia
    if ( $rows ) {
      foreach ( $rows as $course ) {
        $start_time = strtotime($course['jam_mulai']);
        $end_time = strtotime($course['jam_selesai']);

        // Cek apakah waktu saat ini berada di antara jam_mulai dan jam_selesai
        if ( ($current_time >= $start_time) && ($current_time <= $end_time) ) {
          $current_course[] = $course['id_matkul'];
        }
      }
    }
    return $current_course; // return array kosong jika tidak ada jadwal matkul
  }

  // method untuk mengecek apakah uid mahasiswa/i terdaftar
  public function check_student_uid($uid) : bool {
    $query = "SELECT `uid` FROM tbl_mhsw WHERE `uid` = :uid";
    $stmt  = $this->conn->prepare($query);
    $stmt->bindParam(":uid", $uid, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetch(PDO::FETCH_ASSOC);

    if ( $rows ) {
      return true;
    }
    else {
      return false;
    }
  }

  // method untuk mendapatkan NIM mahasiswa/i by uid
  public function get_student_data_by_uid($uid) : ?array {
    $query = "SELECT `kelas`, `NIM` FROM tbl_mhsw WHERE `uid` = :uid";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":uid", $uid, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetch(PDO::FETCH_ASSOC);

    if ( $rows ) {
      return $rows;
    }
    return null;
  }

  // method untuk menambahkan absensi mahasiswa/i
  public function add_student_attendance($current_datetime, $current_time, $nim, $course_id, $status) : bool {
    $query = "INSERT INTO tbl_absen (`hari_tanggal`, `waktu_presensi`, `NIM`, `id_matkul`, `status`) VALUES (:hari_tanggal, :waktu_presensi, :nim, :id_matkul, :status)";
    $stmt = $this->conn->prepare($query);
    $stmt->bindValue(":hari_tanggal", $current_datetime, PDO::PARAM_STR);
    $stmt->bindValue(":waktu_presensi", $current_time, PDO::PARAM_STR);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $stmt->bindParam(":id_matkul", $course_id, PDO::PARAM_STR);
    $stmt->bindParam(":status", $status, PDO::PARAM_STR);
    $result = $stmt->execute();

    if ( !$result ) { // failed
      return false;
    }
    return $result;
  }

  // method untuk menampilkan semua riwayat kehadiran mahasiswa/i
  public function get_all_student_attendances($nim) : ?array {
    $query = "SELECT `hari_tanggal`, `waktu_presensi`, `status` FROM tbl_absen WHERE `NIM` = :nim ORDER BY `waktu_presensi` DESC";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    if ( $rows ) {
      return $rows;
    }
    return null;
  }

  // ------------ YANG KEMARIN ------------
  // method tambah data mahasiswa
  public function add_new_student($nim, $pass, $uid, $name, $class, $telp_num) : bool {    
    $query = "INSERT INTO `tbl_mhsw` (`nim`, `password`, `uid`, `nama`, `kelas`, `no_telp`) VALUES (:nim, :pass, :uid, :nama, :kelas, NULLIF(:no_telp, ''))";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $stmt->bindValue(":pass", password_hash($pass, PASSWORD_DEFAULT), PDO::PARAM_STR);
    $stmt->bindParam(":uid", $uid, PDO::PARAM_STR);
    $stmt->bindParam(":nama", $name, PDO::PARAM_STR);
    $stmt->bindParam(":kelas", $class, PDO::PARAM_STR);
    
    // Menangani no_telp secara terpisah jika menggunakan NULLIF di dalam query
    if ( empty($telp_num) ) {
      $stmt->bindValue(':no_telp', null, PDO::PARAM_NULL);
    }
    else {
      $stmt->bindParam(":no_telp", $telp_num, PDO::PARAM_STR);
    }
    $result = $stmt->execute();
    
    if ( !$result ) { // failed
      return false;
    }

    return $result;
  }

  // fungsi update data mahasiswa by nim
  public function update_student_data($new_name, $new_uid, $nim) : bool {
    $query = "UPDATE `tbl_mhsw` SET `nama` = :nama, `uid` = :uid WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nama", $new_name, PDO::PARAM_STR);
    $stmt->bindParam(":uid", $new_uid, PDO::PARAM_STR);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $result = $stmt->execute();

    if ( !$result ) { // failed
      return false;
    }

    return $result;
  }

  // fungsi hapus data mahasiswa by nim
  public function delete_student_data($nim) : bool {
    $query = "DELETE FROM `tbl_mhsw` WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $result = $stmt->execute();

    if ( !$result ) { // failed
      return false;
    }

    return $result;
  }

  // fungsi cari data mahasiswa (name, nim, or class) by keyword
  public function search_student_data($keyword) : ?array {
    $query = "SELECT * FROM `tbl_mhsw` WHERE `nim` LIKE :keyword OR `nama` LIKE :keyword OR `kelas` LIKE :keyword";
    $stmt = $this->conn->prepare($query);
    $stmt->bindValue(":keyword", "%$keyword%", PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC); // Mengambil hasil pencarian

    if ( $rows ) {
      return $rows;
    }
    return null; // return null
  }

  // fungsi untuk mencari nama mahasiswa by nim
  public function get_student_data_by_nim($nim) : ?array {
    $query = "SELECT `nama` FROM `tbl_mhsw` WHERE `nim` = :nim";
    $stmt = $this->conn->prepare($query);
    $stmt->bindParam(":nim", $nim, PDO::PARAM_STR);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    if ( $rows ) {
      return $rows;
    }
    return null; // return null
  }
  /* -------- CRUDS OPERATION -------- */
}
/* END OF CLASS DbFunctions */

/* ----------------- DbFunctions Object ----------------- */
$config = parse_ini_file('.env');
$db_host = $config['DB_HOST'];
$db_name = $config['DB_NAME'];
$db_user = $config['DB_USER'];
$db_pass = $config['DB_PASS'];

// Instance objek database untuk membuat koneksi baru ke mariadb
$db_functions = new DbFunctions($db_host, $db_name, $db_user, $db_pass);
/* ----------------- DbFunctions Object ----------------- */

/* Class MqttConection */
require __DIR__.'/../library/vendor/autoload.php';
use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;
use \PhpMqtt\Client\Exceptions\MqttClientException;

class MqttConnection {
  private $mqtt_client;
  private $mqtt_broker, $mqtt_port, $client_id, $mqtt_ver;
  private $sub_topic = "SmarTendance/ESP8266", $pub_topic = "SmarTendance/SERVER";
  private $db_functions;

  public function __construct($mqtt_broker, $mqtt_port, $client_id, $mqtt_ver) {
    $this->mqtt_broker = $mqtt_broker;
    $this->mqtt_port = $mqtt_port;
    $this->client_id = $client_id;
    $this->mqtt_ver = $mqtt_ver;
    $this->db_functions = $GLOBALS['db_functions'];
  }

  private function mqtt_connect() {
    $connection_settings = (new ConnectionSettings)
      ->setUsername(null)
      ->setPassword(null)
      ->setKeepAliveInterval(3600)
      ->setConnectTimeout(3)
      //->setUseTls(true)
      //->setTlsSelfSignedAllowed(true)
      ->setLastWillQualityOfService(1);
    
    $clean_session = true; // you can set this to false
    try {
      $this->mqtt_client = new MqttClient($this->mqtt_broker, $this->mqtt_port, $this->client_id, $this->mqtt_ver);
      $this->mqtt_client->connect($connection_settings, $clean_session);
    }
    catch (MqttClientException $e) {
      die('There is a problem while connecting to Mqtt broker. An exception occurred: ' . $e);
    }
  }

  // method getter untuk terkoneksi ke Mqtt broker
  public function get_mqtt_connection() {
    return $this->mqtt_connect();
  }

  // method untuk membaca uid yang dikirim oleh esp8266 (publisher)
  public function presence() {
    $callback = function ($sub_topic, $uid, $retained, $matchedWildcards) {
      echo sprintf("Received message on sub_topic [%s]: %s\n", $sub_topic, $uid);
      
      // Pengecekan untuk UID mahasiswa yang terdaftar
      $student_uid = $this->db_functions->check_student_uid($uid);
      if ( $student_uid ) {
        $current_day = date("D"); // hari saat ini
        switch ( $current_day ) {
          case 'Mon':
            $current_day = "Senin";
            break;
          case 'Tue':
            $current_day = "Selasa";
            break;
          case 'Wed':
            $current_day = "Rabu";
            break;
          case 'Thu':
            $current_day = "Kamis";
            break;
          case 'Fri':
            $current_day = "Jumat";
            break;
          case 'Sat':
            $current_day = "Sabtu";
            break;
          case 'Sun':
            $current_day = "Minggu";
            break;
          default:
            $current_day = "Hari tidak ditemukan";
            break;
        }

        $current_time = strtotime(date("H:i:s")); // Waktu saat ini
        $student_class = $this->db_functions->get_student_data_by_uid($uid)['kelas']; // Mendapatkan kelas mahasiswa berdasarkan uid
        
        $current_course = $this->db_functions->get_current_course($student_class, $current_day, $current_time); // Mendapatkan list jadwal matkul yang tersedia di hari ini
        
        $student_courses = $this->db_functions->get_all_student_courses($student_class); // Mendapatkan semua jadwal matkul mahasiswa

        $course_id = ""; // untuk menampung nama matkul
        $status = ""; // untuk menampung status kehadiran mahasiswa (Hadir, Terlambat, Alpa)

        // Pengecekan untuk jadwal mata kuliah yang tersedia
        if ( !empty($current_course) ) {
          $course_id = $current_course[0]; // set current course

          foreach ( $student_courses as $course ) {
            // Pengecekan jadwal mata kuliah pada hari ini
            if ( $course['hari'] === $current_day ) {
              $start_time = strtotime($course['jam_mulai']);
              $end_time = strtotime($course['jam_selesai']);

              // Pengecekan waktu presensi, jika di antara jam_mulai sampai jam_mulai + 15 menit awal
              if ( ($current_time >= $start_time) && ($current_time <= $start_time + (15 * 60)) ) {
                $status = "Hadir"; // status: Hadir
                break;
              }
              // Jika di antara jam_mulai + 15 menit sampai jam_selesai
              else if ( ($current_time > $start_time + (15 * 60)) && ($current_time <= $end_time) ) {
                $status = "Terlambat"; // status: Terlambat
                break;
              }
              // Terakhir, jika melebihi jam_selesai
              else if ( $current_time > $end_time ) {
                $status = "Alpa"; // status: Alpa
                break;
              }
            }
          }

          // Masukan ke database
          $current_datetime = new DateTime(); // set current datetime format
          $formatted_current_datetime = $current_datetime->format('Y-m-d H:i:s'); // get the current date and time

          $formatted_current_time = date("H:i:s", $current_time); // get the current time

          $student_nim = $this->db_functions->get_student_data_by_uid($uid)['NIM']; // get student nim by uid
          
          // add student attendance to tbl_absen
          $this->db_functions->add_student_attendance($formatted_current_datetime, $formatted_current_time, $student_nim, $course_id, $status);
          echo "[SERVER]: Data berhasil dimasukan ke database\n";
        }
        else {
          $status = "Unavailable course for now";
        }

        // Pesan apabila UID mahasiswa terdaftar
        $message = [
          "keterangan" => "Student UID is registered",
          "status" => $status,
        ];
        // Publish pesannya ke Mqtt broker di topik SmarTendance/SERVER
        $this->mqtt_client->publish($this->pub_topic, json_encode($message), 0);
      }
      
      else {
        // Pesan apabila UID mahasiswa tidak terdaftar
        $message = [ "keterangan" => "Student UID is not registered" ];
        // publish the message in json format
        $this->mqtt_client->publish($this->pub_topic, json_encode($message), 0);
      }
    };

    // Percobaan untuk subscribe ke Mqtt broker di topik SmarTendance/ESP8266
    try {
      $this->mqtt_client->subscribe($this->sub_topic, $callback, 0);
      $this->mqtt_client->loop(true);
      $this->mqtt_client->disconnect();
    }
    // Jika percobaan subscribe gagal
    catch (MqttClientException $e) {
      // Handle exceptions here
      echo "Error: " . $e->getMessage();
    }
  }
}

/* ----------------- MqttConection Object ----------------- */
/* PRIVATE BROKER USING HIVEMQ.CLOUD 
$mqtt_broker = '587dd96c589c4f5b8f049f2d78f8f801.s1.eu.hivemq.cloud';
$mqtt_tls_port = 8883;
$client_id = 'php-mqtt-client';
$mqtt_ver = MqttClient::MQTT_3_1_1;
$username = 'SmarTendance';
$password = 'SmarTendance-MQTT123';
$pub_topic = "SmarTendance/SERVER";
*/

/* LIST PUBLIC MQTT BROKER 
 * broker.hivemq.com  -> https://hivemq.com/
 * broker.emqx.io     -> https://emqx.io/
 * free.mqtt.iyoti.id -> https://iyoti.id/
*/

$mqtt_broker = $config['MQTT_BROKER']; 
$mqtt_port = 1883;
$client_id = $config['MQTT_CLIENT_ID'];
$mqtt_version = MqttClient::MQTT_3_1_1;
// $username = null;
// $password = null;

// Instance objek mqtt_client untuk membuat koneksi baru ke Mqtt broker 
$mqtt_client = new MqttConnection($mqtt_broker, $mqtt_port, $client_id, $mqtt_version);
$mqtt_client->get_mqtt_connection(); // Connect to MQTT broker
/* ----------------- MqttConection Object ----------------- */