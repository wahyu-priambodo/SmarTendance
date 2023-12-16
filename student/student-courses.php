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

$student_name  = $_SESSION['student']['nama_mhsw'];
$student_class = $_SESSION['student']['kelas'];
echo $student_class;
$all_courses = $db_functions->get_all_student_courses($student_class);
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
    <link rel="stylesheet" href="plugins/css/course.css" />
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
        <h3 id="tanggal"></h3>
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
            <h1>Matkul Saya</h1>
            <ul class="breadcrumb">
              <li><a href="" class="active">Course</a></li>
              /
            </ul>
          </div>
        </div>

        <!-- Tabel Course Terdaftar -->
        <div class="bottom-data">
          <div class="orders">
            <div class="header">
              <i class="bx bx-calendar"></i>
              <h3 id="tanggal"></h3>
              <i class="bx bx-filter"></i>
              <i class="bx bx-search"></i>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Nama Matkul</th>
                  <th>ID Matkul</th>
                  <th>Hari</th>
                  <th>Jam Mulai</th>
                  <th>Jam Selesai</th>
                </tr>
              </thead>
              <tbody>
                <?php
                foreach ($all_courses as $course) {
                  echo "<tr>";
                  echo "<td>" . $course['nama_matkul'] . "</td>";
                  echo "<td>" . $course['id_matkul'] . "</td>";
                  echo "<td>" . $course['hari'] . "</td>";
                  echo "<td>" . $course['jam_mulai'] . "</td>";
                  echo "<td>" . $course['jam_selesai'] . "</td>";
                  echo "<td class='edit'><a href='student-attendances.php?nama_matkul=" . $course['nama_matkul'] . "' class='status completed'><i class='bx bxs-chevron-right'></i>lihat</a></td>";
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
    </script>

    <script>
      document.addEventListener("DOMContentLoaded", function () {
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "dark") {
          document.body.classList.add("dark");
          toggler.checked = true;
        }

        // Fungsi untuk memperbarui waktu secara berkala
        function updateClock() {
          const tanggalElement = document.getElementById("tanggal");
          const currentTime = new Date();
          const hari = currentTime.toLocaleDateString(undefined, {
            weekday: "long",
          });
          const tanggal = currentTime.getDate();
          const bulan = currentTime.toLocaleDateString(undefined, {
            month: "long",
          });
          const tahun = currentTime.getFullYear();

          // Format waktu
          const formattedTime = `${hari}, ${tanggal} ${bulan} ${tahun}`;

          // Tampilkan waktu dalam elemen dengan ID "tanggal"
          tanggalElement.textContent = formattedTime;
        }

        // Memanggil fungsi updateClock untuk menampilkan waktu saat halaman dimuat
        updateClock();

        // if admin wants to logout
        document.addEventListener('DOMContentLoaded', function() {
          document.getElementById('confirm-logout').addEventListener('click', function() {
            window.location.href = 'student-logout.php';
          });
        });
      });
    </script>
  </body>
</html>
<?php endif; ?>