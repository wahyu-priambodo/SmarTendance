<?php
// Halaman tambah data mahasiswa
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
    header("Location: login-admin.php");
    exit;
}

require "../fungsi.php";
$admin = new Action();

// logic untuk tambah data mahasiswa baru
if (isset($_POST["create"])) {
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
    <h1 class="text-center mb-4">Tambah Data Mahasiswa</h1>
    <form action="" method="POST">
        <div class="form-group">
            <label for="uid-mahasiswa">UID Mahasiswa</label>
            <input type="text" name="uid" id="uid-mahasiswa" class="form-control" placeholder="Scan Kartu" value="" autofocus autocomplete="off" readonly>
        </div>
        <div class="form-group">
            <label for="nim-mahasiswa">NIM Mahasiswa</label>
            <input type="text" name="nim" id="nim-mahasiswa" class="form-control" placeholder="NIM" autocomplete="off">
        </div>
        <div class="form-group">
            <label for="nama-mahasiswa">Nama Mahasiswa</label>
            <input type="text" name="nama" id="nama-mahasiswa" class="form-control" placeholder="Nama" autocomplete="off">
        </div>
        <div class="form-group">
            <label for="password-mahasiswa">Password Mahasiswa</label>
            <input type="password" name="password" id="password-mahasiswa" class="form-control" placeholder="Password" autocomplete="off">
        </div>
        <div class="form-group">
        <div class="form-group">
            <label for="kelas-mahasiswa">Kelas Mahasiswa</label>
            <select name="kelas" id="kelas-mahasiswa" class="form-control">
                <option value="TMJ-3A">TMJ-3A</option>
                <option value="TMJ-3B">TMJ-3B</option>
                <option value="TKJ-2A">TKJ-2A</option>
                <option value="TKJ-2B">TKJ-2B</option>
            </select>
        </div>
        </div>
        <div class="form-group">
            <label for="no-mahasiswa">No. Telp Mahasiswa</label>
            <input type="text" name="no-telp" id="no-mahasiswa" class="form-control" placeholder="No. Telpon (Opsional)" autocomplete="off">
        </div>
        <button type="submit" name="create" class="btn btn-primary">Tambah Data Mahasiswa</button>
    </form>
</body>

</html>
