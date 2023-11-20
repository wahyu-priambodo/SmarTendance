<?php
// Halaman ubah data mahasiswa
session_start();

if (isset($_COOKIE["admin"]) && $_COOKIE["admin"] !== hash("sha256", $_SESSION["admin"]["nama"])) {
    session_destroy();
    session_unset();
    $_SESSION = [];
    setcookie("admin", "", time() - 14400); // hapus cookie 4 jam ke belakang (3600*4)
    header("Location: login-admin.php");
    exit;
}

if (!isset($_SESSION["admin"])) {
    header("Location: dashboard-admin.php");
    exit;
}

require "../fungsi.php";
$admin = new Action();

// Jika parameter nim ada di url
if (isset($_GET["nim"])) {
    $nimMhsw = htmlspecialchars($_GET["nim"], ENT_QUOTES);
    $namaBaru = htmlspecialchars($_POST["nama-baru"], ENT_QUOTES);
    $uidBaru = htmlspecialchars($_POST["uid-baru"], ENT_QUOTES);
    $mhsw = $admin->getInfoByNim($nimMhsw); // menampilkan nama terkait sesuai parameter nim yang dipassing pada url

    if (isset($_POST["update"])) {
        $admin->updateDataMhsw($namaBaru, $uidBaru, $nimMhsw);
        header("Location: dashboard-admin.php?message=Data mahasiswa berhasil diubah");
        exit;
    }
} else {
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
    <!-- Tambahkan Bootstrap JS (opsional, jika diperlukan) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

    <!-- Tambahkan Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
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
                } else {
                    // Tindakan jika gagal memuat data
                    console.log("Gagal memuat data");
                }
            });
        }
    </script>
    <style>
        body {
            padding: 20px;
        }

        form {
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
</head>

<body>
    <h1 class="text-center mb-4">Ubah Data Mahasiswa</h1>
    <form action="" method="POST">
        <div class="form-group">
            <label for="nama">Nama mahasiswa baru:</label>
            <input type="text" name="nama-baru" id="nama" class="form-control" placeholder="Nama yang baru" value="<?= $mhsw["nama"]; ?>" autofocus autocomplete="off">
        </div>
        <div class="form-group">
            <label for="uid-mahasiswa">UID mahasiswa baru:</label>
            <input type="text" name="uid-baru" id="uid-mahasiswa" class="form-control" placeholder="Scan kartu..." autocomplete="off" readonly>
        </div>
        <button type="submit" name="update" class="btn btn-primary">Update Data Mahasiswa</button>
    </form>
</body>

</html>