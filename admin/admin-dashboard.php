<?php
// Dashboard admin
require __DIR__.'/../config/functions.php';
session_start();
date_default_timezone_set('Asia/Jakarta');

if ( isset($_COOKIE["admin"]) && $_COOKIE["admin"] !== hash("sha256", $_SESSION["admin"]["nama_admin"]) ) {
  session_destroy();
  session_unset();
  $_SESSION = [];
  setcookie('admin', '', time()-(3600*4)); // hapus cookie 4 jam ke belakang
  header('Location: ../index.php');
  exit;
}

if ( !isset($_SESSION["admin"]) ) {
  header('Location: ../index.php');
  exit;
}

$total_students = $db_functions->get_total_students();
$total_lecturers = $db_functions->get_total_lecturers();
$total_courses = $db_functions->get_total_courses();
$total_classes = $db_functions->get_total_classes();
$all_students = $db_functions->get_all_students_data();
$all_lecturers = $db_functions->get_all_lecturers_data();

?>

<?php if ( isset($_SESSION["admin"]) ) : ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="plugins/css/style.css" />
    <link rel="stylesheet" href="plugins/css/SideMenu_Navbar.css" />
    <title>Dashboard Admin</title>
  </head>

  <body>
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="#" class="logo">
        <img src="../assets/logo.png" alt="Logo SmarTandance" />
        <div class="logo-name"><span>Smar</span>Tendance</div>
      </a>
      <ul class="side-menu">
        <li class="active">
          <a href="admin-dashboard.php"><i class="bx bxs-dashboard"></i>Dashboard</a>
        </li>
        <li>
          <a href="course.html"><i class="bx bxs-graduation"></i>Course</a>
        </li>
        <li>
          <a href="registrasi.html"><i class="bx bx-group"></i>Registrasi</a>
        </li>
        <li>
          <a href="#"><i class="bx bxs-door-open"></i>Kelas</a>
        </li>
        <li>
          <a href="rekap_absen.html"><i class="bx bx-data"></i>Rekap Absensi</a>
        </li>
        <li>
          <a href="#"><i class="bx bx-cog"></i>Settings</a>
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
            <h1>Dashboard <?= $_SESSION['admin']['nama_admin'] ?></h1>
            <ul class="breadcrumb">
              <li><a href="admin-dashboard.php" class="active">Dashboard</a></li>
              /
            </ul>
          </div>
        </div>

        <!-- Insights -->
        <ul class="insights">
          <li>
            <i class="bx bx-group"></i>
            <span class="info">
              <h3><?= $total_students ?></h3>
              <p>Mahasiswa Terdaftar</p>
            </span>
          </li>
          <li>
            <i class="bx bxs-user"></i>
            <span class="info">
              <h3><?= $total_lecturers ?></h3>
              <p>Jumlah Dosen</p>
            </span>
          </li>
          <li>
            <i class="bx bxs-graduation"></i>
            <span class="info">
              <h3><?= $total_courses ?></h3>
              <p>Jumlah Course</p>
            </span>
          </li>
          <li>
            <i class="bx bxs-door-open"></i>
            <span class="info">
              <h3><?= $total_classes ?></h3>
              <p>Jumlah Kelas</p>
            </span>
          </li>
        </ul>
        <!-- End of Insights -->

        <!-- Tabel Mahasiswa Terdaftar -->
        <div class="bottom-data">
          <div class="orders" data-table="mahasiswa">
            <div class="header" data-table="mahasiswa">
              <i class="bx bx-table" data-table="mahasiswa"></i>
              <h3>Mahasiswa Terdaftar</h3>
              <div class="filter-dropdown">
                <select id="mahasiswa-data-filter">
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="15">15</option>
                </select>
                <i class="bx bx-filter bx-filter-mahasiswa"></i>
              </div>
              <input
                type="search"
                placeholder="Search..."
                class="search-input"
              />
              <button class="search-btn" type="submit">
                <i class="bx bx-search"></i>
              </button>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Nama Mahasiswa</th>
                  <th class="data">NIM</th>
                  <th class="data">UID</th>
                  <th class="data">Kelas</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <?php
                foreach ($all_students as $student) {
                  echo "<tr>";
                  echo "<td>";
                  echo "<img src='../assets/profile_logo.png' />";
                  echo "<p>{$student['nama_mhsw']}</p>";
                  echo "</td>";
                  echo "<td>{$student['NIM']}</td>";
                  echo "<td>{$student['uid']}</td>";
                  echo "<td>{$student['kelas']}</td>";
                  echo "<td class='action'>";
                  echo "<a href='#' class='status completed'>";
                  echo "<i class='bx bxs-edit ed'></i>ubah";
                  echo "</a>";
                  echo "<a href='#' class='status delete'>";
                  echo "<i class='bx bxs-edit ed'></i>hapus";
                  echo "</a>";
                  echo "</td>";
                  echo "</tr>";
                }
                ?>
              </tbody>
            </table>
            <div class="pagination">
              <button id="mahasiswa-prev-page" disabled>
                <i class="bx bx-chevrons-left"></i>
              </button>
              <span id="mahasiswa-current-page">Page 1</span>
              <button id="mahasiswa-next-page">
                <i class="bx bx-chevrons-right"></i>
              </button>
            </div>
          </div>

          <!-- Tabel Dosen Terdaftar -->

          <div class="orders" data-table="dosen">
            <div class="header" data-table="dosen">
              <i class="bx bx-table" data-table="dosen"></i>
              <h3>Dosen Terdaftar</h3>
              <div class="filter-dropdown">
                <select id="dosen-data-filter">
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="15">15</option>
                </select>
                <i class="bx bx-filter bx-filter-dosen"></i>
              </div>
              <input
                type="search"
                placeholder="Search..."
                class="search-input"
              />
              <button class="search-btn" type="submit">
                <i class="bx bx-search"></i>
              </button>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Nama Dosen</th>
                  <th>NIP</th>
                  <th>Jumlah Matkul</th>
                  <th>Prodi</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <?php
                foreach ($all_lecturers as $lecturer) {
                  echo "<tr>";
                  echo "<td>";
                  echo "<img src='../assets/profile_logo.png' />";
                  echo "<p>{$lecturer['nama_dosen']}</p>";
                  echo "</td>";
                  echo "<td>{$lecturer['NIP']}</td>";
                  echo "<td>{$lecturer['jumlah_matkul']}</td>";
                  echo "<td>{$lecturer['prodi']}</td>";
                  echo "<td class='action'>";
                  echo "<a href='#' class='status completed'>";
                  echo "<i class='bx bxs-edit ed'></i>ubah";
                  echo "</a>";
                  echo "<a href='#' class='status delete'>";
                  echo "<i class='bx bxs-edit ed'></i>hapus";
                  echo "</a>";
                  echo "</td>";
                  echo "</tr>";
                }
                ?>
              </tbody>
            </table>
            <div class="pagination">
              <button id="dosen-prev-page" disabled>
                <i class="bx bx-chevrons-left"></i>
              </button>
              <span id="dosen-current-page">Page 1</span>
              <button id="dosen-next-page">
                <i class="bx bx-chevrons-right"></i>
              </button>
            </div>
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

      const searchButtons = document.querySelectorAll(
        ".bottom-data .orders .header .search-btn"
      );
      const searchButtonIcons = document.querySelectorAll(
        ".bottom-data .orders .header .search-btn .bx"
      );
      const searchInputs = document.querySelectorAll(
        ".bottom-data .orders .header .search-input"
      );

      searchButtons.forEach((searchButton, index) => {
        const searchButtonIcon = searchButtonIcons[index];
        const searchInput = searchInputs[index];

        searchButton.addEventListener("click", function (e) {
          e.preventDefault();
          searchInput.classList.toggle("show");

          if (searchInput.classList.contains("show")) {
            searchButtonIcon.classList.replace("bx-search", "bx-x");
            searchInput.focus(); // Fokuskan input textfield setelah ditampilkan
          } else {
            searchButtonIcon.classList.replace("bx-x", "bx-search");
          }
        });
      });

      // Identifikasi elemen-elemen terkait dengan tabel mahasiswa
      const mahasiswaTable = document.querySelector(
        ".orders[data-table='mahasiswa']"
      );
      const mahasiswaFilterIcon = document.querySelector(
        ".bx-filter-mahasiswa"
      );
      const mahasiswaFilterDropdown =
        mahasiswaTable.querySelector(".filter-dropdown");
      const mahasiswaDataFilterSelect = document.getElementById(
        "mahasiswa-data-filter"
      );
      const mahasiswaTableRows =
        mahasiswaTable.querySelectorAll("table tbody tr");
      const mahasiswaPrevPageButton = document.getElementById(
        "mahasiswa-prev-page"
      );
      const mahasiswaNextPageButton = document.getElementById(
        "mahasiswa-next-page"
      );
      const mahasiswaCurrentPageSpan = document.getElementById(
        "mahasiswa-current-page"
      );

      // Identifikasi elemen-elemen terkait dengan tabel dosen
      const dosenTable = document.querySelector(".orders[data-table='dosen']");
      const dosenFilterIcon = document.querySelector(".bx-filter-dosen");
      const dosenFilterDropdown = dosenTable.querySelector(".filter-dropdown");
      const dosenDataFilterSelect =
        document.getElementById("dosen-data-filter");
      const dosenTableRows = dosenTable.querySelectorAll("table tbody tr");
      const dosenPrevPageButton = document.getElementById("dosen-prev-page");
      const dosenNextPageButton = document.getElementById("dosen-next-page");
      const dosenCurrentPageSpan =
        document.getElementById("dosen-current-page");

      // Mahasiswa
      let currentPageMhs = 1;
      let itemsPerPageMhs = parseInt(mahasiswaDataFilterSelect.value);

      function updatePaginationMahasiswa() {
        const totalPages = Math.ceil(
          mahasiswaTableRows.length / itemsPerPageMhs
        );
        mahasiswaCurrentPageSpan.textContent = `Page ${currentPageMhs}`;

        if (currentPageMhs === 1) {
          mahasiswaPrevPageButton.disabled = true;
        } else {
          mahasiswaPrevPageButton.disabled = false;
        }

        if (currentPageMhs === totalPages) {
          mahasiswaNextPageButton.disabled = true;
        } else {
          mahasiswaNextPageButton.disabled = false;
        }

        mahasiswaTableRows.forEach((row, index) => {
          if (
            index >= (currentPageMhs - 1) * itemsPerPageMhs &&
            index < currentPageMhs * itemsPerPageMhs
          ) {
            row.style.display = "";
          } else {
            row.style.display = "none";
          }
        });
      }

      mahasiswaFilterIcon.addEventListener("click", function () {
        mahasiswaFilterDropdown.classList.toggle("active");
      });

      mahasiswaDataFilterSelect.addEventListener("change", function () {
        itemsPerPageMhs = parseInt(mahasiswaDataFilterSelect.value);
        currentPageMhs = 1;
        updatePaginationMahasiswa();
      });

      mahasiswaPrevPageButton.addEventListener("click", function () {
        if (currentPageMhs > 1) {
          currentPageMhs--;
          updatePaginationMahasiswa();
        }
      });

      mahasiswaNextPageButton.addEventListener("click", function () {
        const totalPages = Math.ceil(
          mahasiswaTableRows.length / itemsPerPageMhs
        );
        if (currentPageMhs < totalPages) {
          currentPageMhs++;
          updatePaginationMahasiswa();
        }
      });

      updatePaginationMahasiswa();

      // dosen
      let currentPageDsn = 1;
      let itemsPerPageDsn = parseInt(dosenDataFilterSelect.value);

      function updatePaginationDosen() {
        const totalPages = Math.ceil(dosenTableRows.length / itemsPerPageDsn);
        dosenCurrentPageSpan.textContent = `Page ${currentPageDsn}`;

        if (currentPageDsn === 1) {
          dosenPrevPageButton.disabled = true;
        } else {
          dosenPrevPageButton.disabled = false;
        }

        if (currentPageDsn === totalPages) {
          dosenNextPageButton.disabled = true;
        } else {
          dosenNextPageButton.disabled = false;
        }

        dosenTableRows.forEach((row, index) => {
          if (
            index >= (currentPageDsn - 1) * itemsPerPageDsn &&
            index < currentPageDsn * itemsPerPageDsn
          ) {
            row.style.display = "";
          } else {
            row.style.display = "none";
          }
        });
      }

      dosenFilterIcon.addEventListener("click", function () {
        dosenFilterDropdown.classList.toggle("active");
      });

      dosenDataFilterSelect.addEventListener("change", function () {
        itemsPerPageDsn = parseInt(dosenDataFilterSelect.value);
        currentPageDsn = 1;
        updatePaginationDosen();
      });

      dosenPrevPageButton.addEventListener("click", function () {
        if (currentPageDsn > 1) {
          currentPageDsn--;
          updatePaginationDosen();
        }
      });

      dosenNextPageButton.addEventListener("click", function () {
        const totalPages = Math.ceil(dosenTableRows.length / itemsPerPageDsn);
        if (currentPageDsn < totalPages) {
          currentPageDsn++;
          updatePaginationDosen();
        }
      });

      updatePaginationDosen();

      // if admin wants to logout
      document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('confirm-logout').addEventListener('click', function() {
          window.location.href = 'admin-logout.php';
        });
      });
    </script>
  </body>
</html>
<?php endif; ?>