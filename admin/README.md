<div align="center"> <h1>Progres 3 by Wahyu</h1> </div>

## Problem yang dialami & solusinya:

- Antara server Apache di XAMPP dan ESP8266 harus berada di dalam 1 jaringan, sehingga harus dikonfigurasi **Listen IP address** pada setingan `httpd.conf`.
  - **Solusi** : Mengubah **Listen** pada file tersebut dengan IP Address laptop (Hotspot)
  
  ```apache
  Listen 192.168.4.127:80
  ```

- Koneksi ke database MySQL menjadi error, karena tidak bisa menjangkau localhost setelah sebelumnya telah terkoneksi dengan IP Server (Hotspot).
  - **Solusi** : Tambahkan user root di host IP Server
  
  ```sql
  CREATE USER 'root'@'192.168.4.127' IDENTIFIED BY '';
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.4.127' WITH GRANT OPTION;
  FLUSH PRIVILEGES;

  /* Melihat daftar user dan host di tabel mysql.user */
  SELECT User, Host FROM mysql.user;
  ```

## Fitur-fitur yang diselesaikan:

- [X] Berhasil mengirimkan data uid dari **Arduino Uno R3** ke **NodeMCU ESP8266** menggunakan pin Rx - Tx (Serial Communication).
- [X] Berhasil menyelesaikan fitur login untuk **admin, mahasiswa, dan dosen** + menggunakan fungsi **`htmlspecialchars`** untuk menghindari serangan XSS.
- [X] Berhasil menambahkan **`$_SESSION`** dan **`$_COOKIE`** untuk menyimpan informasi user yang telah login (on server-side and client-side).
- [X] Berhasil menambahkan operasi **CRUD'S** (Create, Read, Update, Delete, dan Search) untuk mengelola data mahasiswa.
  - [X] `createDataMhsw()` // tambah data mahasiswa baru + uid kartu/tag RFID ke tbl_mhsw
  - [X] `readDataMhsw()` // baca semua data yang ada di tbl_mhsw
  - [X] `updateDataMhsw()` // ubah data mahasiswa, bisa nama dan/atau uid
  - [X] `deleteDataMhsw()` // hapus data mahasiswa sesuai data nim yang diberikan
  - [X] `cariDataMhsw()` // cari data mahasiswa berdasarkan nim, nama, dan kelas sesuai dengan yang tersedia di database
  - [X] `getInfoByNim()` // tampilkan nama mahasiswa berdasarkan data nim yang diberikan
- [X] Berhasil menampilkan data uid kartu/tag rfid ke web PHP dengan bantuan jQuery (AJAX) **(handle-rfid)**.

## TODO:

- [ ] Menghubungkan dengan **frontend**.
- [ ] Tambah **mini buzzer** dan **LCD 16x2 I2C**.
- [ ] Membuat **endpoint + tabel baru di database** untuk menyimpan waktu dan keterangan presensi mahasiswa.