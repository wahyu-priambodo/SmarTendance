-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 04 Nov 2023 pada 06.31
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_course`
--

CREATE TABLE `tbl_course` (
  `id_matkul` int(8) NOT NULL COMMENT 'Kode unik setiap mata kuliah',
  `nama_matkul` varchar(50) NOT NULL COMMENT 'Nama mata kuliah',
  `enroll_code` varchar(8) NOT NULL COMMENT 'Kode untuk enroll course',
  `NIP` varchar(18) NOT NULL COMMENT 'Nomor Identitas Pegawai Negeri Sipil yang dimiliki dosen',
  `deskripsi` varchar(100) DEFAULT NULL COMMENT 'Deskripsi mengenai matakuliah atau cource'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_course`
--

INSERT INTO `tbl_course` (`id_matkul`, `nama_matkul`, `enroll_code`, `NIP`, `deskripsi`) VALUES
(1, 'Sistem Embedded', 'D82HF	', '197910062003122001', 'Bisa kan ya, kalian bisa kan?'),
(2, 'Pemrograman Berorientasi Objek', 'D82HF	', '198501292010121003', 'Coba kamu present dulu');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_dosen`
--

CREATE TABLE `tbl_dosen` (
  `NIP` varchar(18) NOT NULL COMMENT 'Nomor Identitas Pegawai Negeri Sipil yang dimiliki dosen',
  `nama_dosen` varchar(50) NOT NULL COMMENT 'Nama Dosen',
  `password` varchar(100) NOT NULL COMMENT 'Password akun milik dosen',
  `uuid` varchar(50) NOT NULL COMMENT 'Nomor unik dari kartu RFID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_dosen`
--

INSERT INTO `tbl_dosen` (`NIP`, `nama_dosen`, `password`, `uuid`) VALUES
('197509152003122003', 'Maria Agustin', '197509152003122003', 'SBifg38r'),
('197910062003122001', 'Prihatin Oktivasari', '197910062003122001', 'SBifg38r'),
('198112012015041001', 'Defiana Arnaldy', '198112012015041001', 'SBifg38r'),
('198501292010121003', 'Ariawan Andi Suhandana', '198501292010121003', 'SBifg38r'),
('198605222023212032', 'Susana Dwi Yulianti', '198605222023212032', 'SBifg38r'),
('198910112018032002', 'Ayu Rosyida Zain', '198910112018032002', 'SBifg38r'),
('199109262019031012', 'Asep Kurniawan', '199109262019031012', 'SBifg38r'),
('199206052022032008', 'Ratna Widya Iswara', '199206052022032008', 'SBifg38r'),
('199408202022031009', 'Iik Muhamad Malik Matin', '199408202022031009', 'SBifg38r');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_enroll`
--

CREATE TABLE `tbl_enroll` (
  `NIM` varchar(10) NOT NULL COMMENT 'NIM Mahasiswa',
  `id_matkul` int(8) NOT NULL COMMENT 'Kode unik setiap mata kuliah'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_enroll`
--

INSERT INTO `tbl_enroll` (`NIM`, `id_matkul`) VALUES
('2207421031', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbl_mhsw`
--

CREATE TABLE `tbl_mhsw` (
  `NIM` varchar(10) NOT NULL COMMENT 'NIM Mahasiswa',
  `nama_mhsw` varchar(50) NOT NULL COMMENT 'Nama mahasiswa (akun)',
  `password` varchar(255) NOT NULL COMMENT 'Password akun website absensi',
  `kelas` enum('TMJ-3A','TMJ-3B') NOT NULL COMMENT 'Kelas dari mahasiswa',
  `uuid` varchar(50) NOT NULL COMMENT 'Nomor unik dari kartu RFID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tbl_mhsw`
--

INSERT INTO `tbl_mhsw` (`NIM`, `nama_mhsw`, `password`, `kelas`, `uuid`) VALUES
('2207421031', 'Muhammad Khairu Mufid', '2207421031	', 'TMJ-3B', 'SBifg38r'),
('2207421032', 'Kevin Alonzo Manuel Bakara', '2207421032', 'TMJ-3B', 'SBifg38r'),
('2207421048', 'Wahyu Priambodo', '2207421048', 'TMJ-3B', 'SBifg38r');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tbl_course`
--
ALTER TABLE `tbl_course`
  ADD PRIMARY KEY (`id_matkul`),
  ADD KEY `tbl_course_FK` (`NIP`);

--
-- Indeks untuk tabel `tbl_dosen`
--
ALTER TABLE `tbl_dosen`
  ADD PRIMARY KEY (`NIP`);

--
-- Indeks untuk tabel `tbl_enroll`
--
ALTER TABLE `tbl_enroll`
  ADD KEY `tbl_enroll_FK` (`NIM`),
  ADD KEY `tbl_enroll_FK_1` (`id_matkul`);

--
-- Indeks untuk tabel `tbl_mhsw`
--
ALTER TABLE `tbl_mhsw`
  ADD PRIMARY KEY (`NIM`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tbl_course`
--
ALTER TABLE `tbl_course`
  MODIFY `id_matkul` int(8) NOT NULL AUTO_INCREMENT COMMENT 'Kode unik setiap mata kuliah', AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tbl_course`
--
ALTER TABLE `tbl_course`
  ADD CONSTRAINT `tbl_course_FK` FOREIGN KEY (`NIP`) REFERENCES `tbl_dosen` (`NIP`);

--
-- Ketidakleluasaan untuk tabel `tbl_enroll`
--
ALTER TABLE `tbl_enroll`
  ADD CONSTRAINT `tbl_enroll_FK` FOREIGN KEY (`NIM`) REFERENCES `tbl_mhsw` (`NIM`),
  ADD CONSTRAINT `tbl_enroll_FK_1` FOREIGN KEY (`id_matkul`) REFERENCES `tbl_course` (`id_matkul`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
