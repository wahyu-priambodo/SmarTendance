# Progres 2 By Wahyu

## Spesifikasi Backend & Database:
- Software: XAMPP
- Backend: PHP versi 8.2.4
- Database: MariaDB versi 10.4.28

## Fitur yang Sukses Ditambahkan:
- Mahasiswa/i berhasil login dan masuk dashboard Mahasiswa/i
- Diimplementasikan menggunakan konsep paradigma OOP (Object-Oriented Programming)
- Berhasil menghubungkan PHP dengan database menggunakan ekstensi PDO
- Menggunakan fungsi `password_hash()` untuk hashing password mahasiswa
- Menambahkan prevention serangan XSS pada form login dengan fungsi `htmlspecialchars()`
- Menambahkan pesan kesalahan error ketika mahasiswa/i salah menginputkan username dan/atau password

## Struktur Database Saat Ini:
- DB_NAME=`SmarTendance`
- TABLE_NAME=`tbl_mhsw`
- COLUMNS_LIST=`{nim, nama, password, usia, kelas, jenis_kelamin, no_hp, alamat}`