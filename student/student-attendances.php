<?php
// student courses
require __DIR__.'/../config/functions.php';
session_start();
date_default_timezone_set('Asia/Jakarta');

if ( isset($_COOKIE["student"]) && $_COOKIE["student"] !== hash("sha256", $_SESSION["student"]["nama_mhsw"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie('student', '', time()-(3600*4)); // hapus cookie 4 jam ke belakang
  header('Location: ../index.php');
  exit;
}

if ( !isset($_SESSION["student"]) ) {
  header('Location: ../index.php');
  exit;
}

$course_name = $_GET['nama_matkul'];
$student_nim  = $_SESSION['student']['NIM'];
$all_attendances = $db_functions->get_all_student_attendances($student_nim);
?>

<?php if ( isset($_SESSION['student']) ) : ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="plugins/css/data_mhsw.css" />
    <link rel="stylesheet" href="plugins/css/SideMenu_Navbar.css" />
    <title>SmarTendance</title>
  </head>

  <body>
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="#" class="logo">
        <img src="../assets/logo.png" alt="Logo SmarTandance" />
        <div class="logo-name"><span>SmarTendance</span></div>
      </a>
      <ul class="side-menu">
        <li>
          <a href="student-dashboard.php"><i class="bx bxs-dashboard"></i>Dashboard</a>
        </li>
        <li class="active">
          <a href="student-courses.php"><i class="bx bxs-graduation"></i>Course</a>
        </li>
      </ul>
      <ul class="side-menu">
        <li>
          <a href="#" class="logout" id="logout-button">
            <i class="bx bx-log-out-circle"></i>
            Logout
          </a>
          <div class="confirmation-modal" id="confirmation-modal">
            <div class="modal-content">
              <h2>Logout Confirmation</h2>
              <p>Apakah Anda yakin ingin logout?</p>
              <div class="modal-buttons">
                <button id="confirm-logout">Ya</button>
                <button id="cancel-logout">Tidak</button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <!-- End of Sidebar -->

    <!-- Main Content -->
    <div class="content">
      <!-- Navbar -->
      <nav>
        <i class="bx bx-menu"></i>
        <form action="#">
          <div class="form-input">
            <input type="search" placeholder="Search..." />
            <button class="search-btn" type="submit">
              <i class="bx bx-search"></i>
            </button>
          </div>
        </form>
        <input type="checkbox" id="theme-toggle" hidden />
        <label for="theme-toggle" class="theme-toggle"> </label>
        <a href="#" class="profile">
          <img src="../assets/profile_logo.png" />
        </a>
      </nav>
      <!-- End of Navbar -->

      <main>
        <div class="header">
          <div class="left">
            <h1>Course Saya</h1>
            <ul class="breadcrumb">
              <a href="student-courses.php"><li>Course</li></a>
              /
              <li><a href="" class="active"><?= $course_name ?></a></li>
            </ul>
          </div>
        </div>

        <!-- Tabel Course Terdaftar -->
        <div class="bottom-data">
          <div class="orders">
            <div class="header">
              <i class="bx bxs-book-alt"></i>
              <h3><?= $course_name ?></h3>
              <i class="bx bx-filter"></i>
              <i class="bx bx-search"></i>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Hari/Tanggal</th>
                  <th>Waktu Presensi</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <?php
                foreach ($all_attendances as $attendance) {
                  echo "<tr>";
                  // kolom hari/tanggal
                  echo "<td>";
                  echo "<i class='bx bx-calendar'></i>";
                  // Mengubah format tanggal dari 'Y-m-d H:i:s' menjadi 'l, d-m-Y'
                  $formatted_date = date('l, d-m-Y', strtotime($attendance['hari_tanggal']));
                  echo "<p>" . $formatted_date . "</p>";
                  echo "</td>";

                  // kolom waktu presensi
                  echo "<td>";
                  echo "<p>" . $attendance['waktu_presensi'] . "</p>";
                  echo "</td>";

                  // kolom status kehadiran
                  echo "<td class='" . $attendance['status'] . "'>";
                  if ($attendance['status'] === 'Hadir') {
                    echo "<a class='status_completed'>" . $attendance['status'] . "</a>";
                  }
                  else if ($attendance['status'] === 'Terlambat' || $attendance['status'] === 'Alpa') {
                    echo "<a class='status_incompleted'>" . $attendance['status'] . "</a>";
                  }
                  echo "</td>";
                  echo "</tr>";
                }
                ?>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
    <script src="plugins/js/index.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "dark") {
          document.body.classList.add("dark");
          toggler.checked = true;
        }
      });

      // if admin wants to logout
      document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('confirm-logout').addEventListener('click', function() {
          window.location.href = 'student-logout.php';
        });
      });
    </script>
  </body>
</html>
<?php endif; ?>