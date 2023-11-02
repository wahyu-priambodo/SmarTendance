<?php
// Halaman tambah data mahasiswa
session_start();

if ( isset($_COOKIE["admin"]) && $_COOKIE["admin"] !== hash("sha256", $_SESSION["admin"]["nama"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("admin", "", time()-14400); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login-admin.php");
  exit;
}

if ( !isset($_SESSION["admin"]) ) {
  header("Location: login-admin.php");
  exit;
}

require "../fungsi.php";
$admin = new Action();

// logic untuk tambah data mahasiswa baru
if ( isset($_POST["create"]) ) {
  $nimMhsw = htmlspecialchars($_POST["nim"], ENT_QUOTES);
  $passMhsw = htmlspecialchars($_POST["password"], ENT_QUOTES);
  $uidMhsw = htmlspecialchars($_POST["uid"], ENT_QUOTES);
  $namaMhsw = htmlspecialchars($_POST["nama"], ENT_QUOTES);
  $kelasMhsw = htmlspecialchars($_POST["kelas"], ENT_QUOTES);
  $noTelpMhsw = isset($_POST["no-telp"]) ? htmlspecialchars($_POST["no-telp"], ENT_QUOTES) : null;

  $addData = $admin->createDataMhsw($nimMhsw, $passMhsw, $uidMhsw, $namaMhsw, $kelasMhsw, $noTelpMhsw);

  header("Location: dashboard-admin.php?message=Data mahasiswa berhasil ditambahkan");
  exit;
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tambah Data Mahasiswa</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script type="text/javascript">
    $(document).ready(function() {
        // Memuat data uid saat halaman dimuat
        loadDataUid();
        // Memuat data uid setiap detik
        setInterval(loadDataUid, 0);
      });

      function loadDataUid() {
        $("#uid-mahasiswa").load("handle-rfid/read-uid.php", function(response, status, xhr) {
          if (status == "success") {
          // Mengubah value dari input dataUid dengan data uid yang sesungguhnya
          $("#uid-mahasiswa").val(response);
          }
          else {
          // Tindakan jika gagal memuat data
          console.log("Gagal memuat data");
          }
      });
    }
  </script>
</head>
<body>
  <form action="" method="POST">
    <label for="uid-mahasiswa">UID Mahasiswa</label>
    <input type="text" name="uid" id="uid-mahasiswa" placeholder="Scan Kartu" value="" size="50" autofocus autocomplete="off" /><br>

    <label for="nim-mahasiswa">NIM Mahasiswa</label>
    <input type="text" name="nim" id="nim-mahasiswa" placeholder="NIM" size="50" autocomplete="off" /><br>

    <label for="nama-mahasiswa">Nama Mahasiswa</label>
    <input type="text" name="nama" id="nama-mahasiswa" placeholder="Nama" size="50" autocomplete="off" /><br>

    <label for="password-mahasiswa">Password Mahasiswa</label>
    <input type="password" name="password" id="password-mahasiswa" placeholder="Password" size="50" autocomplete="off" /><br>

    <label for="kelas-mahasiswa">Kelas Mahasiswa</label>
    <input type="text" name="kelas" id="kelas-mahasiswa" placeholder="Kelas" size="50" autocomplete="off" /><br>

    <label for="no-mahasiswa">No. Telp Mahasiswa</label>
    <input type="text" name="no-telp" id="no-mahasiswa" placeholder="No. Telpon" size="50" autocomplete="off" /><br>

    <button type="submit" name="create">Tambah</button>
  </form>
</body>
</html>