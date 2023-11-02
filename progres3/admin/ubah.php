<?php
// Halaman ubah data mahasiswa
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
  header("Location: dashboard-admin.php");
  exit;
}

require "../fungsi.php";
$admin = new Action();

// Jika parameter nim ada di url
if ( isset($_GET["nim"]) ) {
  $nimMhsw = htmlspecialchars($_GET["nim"], ENT_QUOTES);
  $namaBaru = htmlspecialchars($_POST["nama-baru"], ENT_QUOTES);
  $uidBaru = htmlspecialchars($_POST["uid-baru"], ENT_QUOTES);
  $mhsw = $admin->getInfoByNim($nimMhsw); // menampilkan nama terkait sesuai parameter nim yang dipassing pada url

  if ( isset($_POST["update"]) ) {
    $admin->updateDataMhsw($namaBaru, $uidBaru, $nimMhsw);
    header("Location: dashboard-admin.php?message=Data mahasiswa berhasil diubah");
    exit;
  }
}
else {
  header("Location: dashboard-admin.php?message=NIM tidak dikenal!");
  exit;
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ubah Data Mahasiswa</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script type="text/javascript">
    $(document).ready(function() {
        // Memuat data uid saat halaman dimuat
        loadDataUid();
        // Memuat data uid setiap detik
        setInterval(loadDataUid, 0);
      });

      function loadDataUid() {
        $("#uid").load("handle-rfid/read-uid.php", function(response, status, xhr) {
          if (status == "success") {
          // Mengubah value dari input dataUid dengan data uid yang sesungguhnya
          $("#uid").val(response);
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
  <p>Ubah data mahasiswa</p>
  <form action="" method="POST">
    <label for="nama">Nama mahasiswa baru: </label>
    <input type="text" name="nama-baru" id="nama" placeholder="Nama yang baru" value="<?= $mhsw["nama"]; ?>" size="50" autofocus autocomplete="off" /><br>
    <label for="uid">UID mahasiswa baru: </label>
    <input type="text" name="uid-baru" id="uid" placeholder="Scan kartu..." value="" size="50" autocomplete="off" /><br>
    <button type="submit" name="update">Update Data Mahasiswa</button>
  </form>
</body>
</html>