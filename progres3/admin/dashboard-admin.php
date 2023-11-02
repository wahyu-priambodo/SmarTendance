<?php
// Dashboard admin
session_start();

if ( isset($_COOKIE["admin"]) && $_COOKIE["admin"] !== hash("sha256", $_SESSION["admin"]["nama"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie("admin", "", time()-(4*3600)); // hapus cookie 4 jam ke belakang (3600*4)
  header("Location: login-admin.php");
  exit;
}

if ( !isset($_SESSION["admin"]) ) {
  header("Location: login-admin.php");
  exit;
}

require "../fungsi.php";
$admin = new Action();

// logic untuk melakukan pencarian
if ( isset($_POST["cari"]) ) {
  $keyword = $_POST["keyword"];
  $dataMhsw = $admin->cariDataMhsw($keyword);
}
else {
  $dataMhsw = $admin->readDataMhsw(); // Jika tidak melakukan pencarian, tampilkan semua data
}

// logic untuk mengambil parameter message saat data berhasil diubah/dihapus
if ( isset($_GET["message"]) ) {
  echo "<script>alert('" . $_GET["message"] . "');</script>";
  echo "<script>window.history.replaceState(null, null, window.location.pathname);</script>";
}

?>

<?php if ( isset($_SESSION["admin"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Admin</title>
</head>
<body>
  <h1>Selamat datang, <?= $_SESSION["admin"]["nama"]; ?></h1>
  <p>hashed value admin di cookie: <strong> <?= $_COOKIE["admin"]; ?></strong></p>
  <p>hashed nama admin: <strong> <?= hash("sha256", $_SESSION["admin"]["nama"]); ?></strong></p><br>

  <form action="" method="POST">
    <label for="keyword">Cari Mahasiswa: </label>
    <input type="text" name="keyword" id="keyword" placeholder="Nama / NIM / Kelas" size="50" autofocus autocomplete="off" />
    <button type="submit" name="cari">Cari!</button>
  </form>

  <table border="1">
    <tr>
      <th>No</th>
      <th>Aksi</th>
      <th>NIM</th>
      <th>Nama</th>
      <th>UID</th>
      <th>Kelas</th>
    </tr>

  <!-- tampilkan semua data mahasiswa kecuali password -->
  <?php $i = 1; ?>
  <?php foreach ($dataMhsw as $mhsw) : ?>
    <tr>
      <td><?= $i++; ?></td>
      <td>
        <a href="ubah.php?nim=<?= $mhsw["nim"] ?>">ubah</a> |
        <a href="hapus.php?nim=<?= $mhsw["nim"] ?>" onclick="return confirm('Apakah Anda yakin ingin menghapus data ini?');">hapus</a>
      </td>
      <td><?= $mhsw["nim"] ?></td>
      <td><?= $mhsw["nama"] ?></td>
      <td><?= $mhsw["uid"] ?></td>
      <td><?= $mhsw["kelas"] ?></td>
    </tr>
  <?php endforeach; ?>
  </table>
  <br>

  <a href="tambah.php">Tambah Data Mahasiswa</a><br>
  <a href="logout-admin.php">Logout</a>
</body>
</html>
<?php endif; ?>