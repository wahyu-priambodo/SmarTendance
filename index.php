<?php
require __DIR__.'/config/functions.php';
session_start();

// check if the student is using cookie (remember-me)
if ( isset($_COOKIE['student']) && $_COOKIE['student'] === hash('sha256', $student_session['nama_mhsw']) ) {
  $_SESSION['student'] = $student_session;
}

// check if the session is already set
if ( isset($_SESSION['student']) ) {
  header('Location: ./student/student-dashboard.php');
  exit;
}

// logic for login student
if ( isset($_POST['login-btn']) && $_SERVER['REQUEST_METHOD'] === "POST" ) {
  if ( isset($_POST['nim']) && isset($_POST['password']) ) {
    $nim = htmlspecialchars($_POST['nim'], ENT_QUOTES);
    $password = htmlspecialchars($_POST['password'], ENT_QUOTES);

    // login student
    $student_session = $db_functions->get_student_login($nim, $password);
    if ( $student_session ) {
      // set student session
      $_SESSION['student'] = $student_session;
      // if the student is using cookie (remember-me)
      if ( isset($_POST['remember-me']) ) {
        // set cookie for 2 hours
        setcookie('student', hash('sha256', $student_session['nama_mhsw']), time()+(3600*2)); 
      }

      header('Location: ./student/student-dashboard.php');
      exit;
    }
    else {
      echo "<script>alert('Login gagal');</script>";
    }
  }
}
?>

<?php if ( !isset($_SESSION['student']) ) : ?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" type="text/css" href="student/plugins/css/login_mhsw.css" />
	<title>SmarTendance</title>
</head>
<body>
	<header class="header">
    <a href="#" class="logo"><img src="assets/logo.png" alt="E-learning PNJ Logo" width="125" height="75"><p style="margin-left: 20px"></p> SmarTendance</p></a>
		<nav class="nav">
			<a href="contact.html" target="_blank">Contact</a>
			<a href="tutorial.html" target="_blank">Tutorial</a>
			<a href="index.php">Login</a>
		</nav>
	</header>

	<section class="Login">
		<div class="content">
			<h2>Selamat datang di portal SmarTendance</h2>
			<p>Silahkan memasukan NIM dan Password Anda!</p>
			<a href="#">Get Started</a>
		</div>

		<div class="wrapper-login">
			<h2>Login Mahasiswa</h2>
			<form action="" method="POST">
				<div class="input-box">
					<span class="icon"><ion-icon name="mail"></ion-icon></span>
					<input type="text" name="nim" id="nim" autocomplete="off" required />
          <label>NIM</label>
				</div>
				<div class="input-box">
					<span class="icon"><ion-icon name="lock-closed"></ion-icon></span>
					<input type="password" name="password" id="password" autocomplete="off" required />
					<label>Password</label>
					<span class="show-password" onclick="togglePasswordVisibility()"><ion-icon name="eye"></ion-icon></span>
				</div>
        <div class="remember">
          <input type="checkbox" id="remember-me" name="remember-me">
          <label>Remember me</label><br>
        </div>
				<button type="submit" class="btn" name="login-btn">Login!</button>
				<div class="jenis">
					<p>
            <a href="lecturer/login.php" target="_blank">Login Dosen</a> / <a href="admin/login.php" target="_blank">Login Admin</a>
          </p>
				</div>
			</form>
		</div>
	</section>

	<script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
	<script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
	<script>
		function togglePasswordVisibility() {
			const passwordInput = document.getElementById("password");
			const eyeIcon = document.querySelector(".show-password ion-icon");
		
			if (passwordInput.type === "password") {
				passwordInput.type = "text";
				eyeIcon.name = "eye-off";
			} else {
				passwordInput.type = "password";
				eyeIcon.name = "eye";
			}
		}
		</script>
</body>
</html>
<?php endif; ?>