-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 20, 2023 at 10:20 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SmarTendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_absen`
--

CREATE TABLE `tbl_absen` (
  `hari_tanggal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'rincian/log waktu ketika mahasiswa melakukan tap/absensi',
  `waktu_presensi` time NOT NULL COMMENT 'waktu presensi',
  `NIM` varchar(10) NOT NULL COMMENT 'NIM dari mahasiswa yang melakukan absensi',
  `id_matkul` varchar(10) NOT NULL COMMENT 'id dari mata kuliah',
  `status` enum('Hadir','Terlambat','Alpa') NOT NULL COMMENT 'Status Kehadiran Mahasiswa/i'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_absen`
--

INSERT INTO `tbl_absen` (`hari_tanggal`, `waktu_presensi`, `NIM`, `id_matkul`, `status`) VALUES
('2023-11-20 02:13:28', '09:13:28', '2207421048', 'RPL2', 'Hadir'),
('2023-11-20 02:13:51', '09:13:51', '2207421048', 'RPL2', 'Hadir'),
('2023-11-20 02:29:20', '09:29:20', '2207421048', 'RPL2', 'Terlambat'),
('2023-11-20 02:50:21', '09:50:21', '2207421048', 'RPL2', 'Terlambat'),
('2023-11-20 02:50:30', '09:50:30', '2207421048', 'RPL2', 'Terlambat'),
('2023-11-20 03:15:21', '10:15:21', '2207421048', 'RPL2', 'Terlambat'),
('2023-11-20 03:17:15', '10:17:15', '2207421048', 'RPL2', 'Terlambat');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_admin`
--

CREATE TABLE `tbl_admin` (
  `id_admin` varchar(20) NOT NULL COMMENT 'nomor id dari admin',
  `nama_admin` varchar(70) NOT NULL COMMENT 'Nama admin',
  `password` varchar(255) NOT NULL COMMENT 'password akun admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_admin`
--

INSERT INTO `tbl_admin` (`id_admin`, `nama_admin`, `password`) VALUES
('1234', 'Admin 1', '$2y$10$nI34Hk3xfCM6xj6apfRkLeVxGDYmLMCSU5IB5KvvgZN6YnaIOV1k6'),
('2345', 'Admin 2', '$2y$10$g1lfHWxJv6xjUW8xVumou.ImKL/AAus4.rzKMMdcqb/CfUFFNbNn.'),
('3456', 'Admin 3', '$2y$10$UfaXARgVjH3fiiWDT6CP3.XDfX.wQEz8C6Dutx33AK3FlJcdgRwwO'),
('4567', 'Admin 4', '$2y$10$AgcqrP8/tUE.oztf1jAjEu/NeESIstTuppsqxpEhCwOtIDbGcwl4W'),
('5678', 'Admin 5', '$2y$10$myx76ys1tltKmYod6CaWze96jwF5R3eUspfUwPqLsME3.VvECMXFG');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_course`
--

CREATE TABLE `tbl_course` (
  `id_matkul` varchar(10) NOT NULL COMMENT 'Kode unik setiap mata kuliah',
  `nama_matkul` varchar(100) NOT NULL COMMENT 'Nama Matkul',
  `SKS` int(2) NOT NULL COMMENT 'SKS matkul',
  `NIP` varchar(18) NOT NULL COMMENT 'NIP Dosen',
  `kelas` varchar(10) NOT NULL COMMENT 'Kelas Mahasiswa/i',
  `hari` enum('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu') NOT NULL,
  `jam_mulai` time NOT NULL COMMENT 'Jam mata kuliah dimulai',
  `jam_selesai` time NOT NULL COMMENT 'Jam mata kuliah selesai'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_course`
--

INSERT INTO `tbl_course` (`id_matkul`, `nama_matkul`, `SKS`, `NIP`, `kelas`, `hari`, `jam_mulai`, `jam_selesai`) VALUES
('COMPSEC1', 'KEAMANAN KOMPUTER-TMJ3A GANJIL', 2, '198112012015041001', 'TMJ-3A', 'Selasa', '08:30:00', '10:30:00'),
('COMPSEC2', 'KEAMANAN KOMPUTER-TMJ3B GANJIL', 2, '198112012015041001', 'TMJ-3B', 'Rabu', '13:00:00', '14:50:00'),
('ENG1', 'ENGLISH FOR IT PROFESSIONAL-TMJ3A GANJIL', 2, '199206052022032008', 'TMJ-3A', 'Selasa', '08:00:00', '10:00:00'),
('ENG2', 'ENGLISH FOR IT PROFESSIONAL-TMJ3B GANJIL', 2, '199206052022032008', 'TMJ-3B', 'Senin', '13:00:00', '15:00:00'),
('INFRA2', 'INFRASTRUKTUR JARINGAN-TMJ3B GANJIL', 2, '199109262019031012', 'TMJ-3B', 'Jumat', '13:30:00', '15:00:00'),
('METNUM2', 'METODE NUMERIK-TMJ3B GANJIL', 1, '199408202022031009', 'TMJ-3B', 'Selasa', '09:00:00', '10:00:00'),
('ORKOM2', 'ORGANISASI DAN ARSITEKTUR KOMPUTER-TMJ3B GANJIL', 2, '198910112018032002', 'TMJ-3B', 'Kamis', '08:30:00', '10:50:00'),
('PBO2', 'PEMROGRAMAN BERORIENTASI OBYEK-TMJ3B GANJIL', 2, '198501292010121003', 'TMJ-3B', 'Selasa', '13:30:00', '15:45:00'),
('RPL2', 'REKAYASA PERANGKAT LUNAK-TMJ3B GANJIL', 2, '198605222023212032', 'TMJ-3B', 'Senin', '09:00:00', '10:30:00'),
('SISMBD2', 'SISTEM EMBEDDED-TMJ3B GANJIL', 2, '197910062003122001', 'TMJ-3B', 'Kamis', '13:30:00', '15:30:00'),
('WEB1', 'PEMROGRAMAN WEB-TMJ3A GANJIL', 2, '197509152003122003', 'TMJ-3A', 'Rabu', '13:00:00', '15:00:00'),
('WEB2', 'PEMROGRAMAN WEB-TMJ3B GANJIL', 2, '197509152003122003', 'TMJ-3B', 'Rabu', '08:00:00', '09:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_dosen`
--

CREATE TABLE `tbl_dosen` (
  `NIP` varchar(18) NOT NULL COMMENT 'Nomor Identitas Pegawai Negeri Sipil yang dimiliki dosen',
  `nama_dosen` varchar(70) NOT NULL COMMENT 'Nama Dosen',
  `password` varchar(255) NOT NULL COMMENT 'Password akun milik dosen',
  `prodi` enum('TMJ','TKJ','TI','TMD') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_dosen`
--

INSERT INTO `tbl_dosen` (`NIP`, `nama_dosen`, `password`, `prodi`) VALUES
('197509152003122003', 'Maria Agustin', '$2y$10$YYx3qISar.zzEdfPivQnMevN8KTXxWXeNRs4jJ1sPmEwWq31YypOO', 'TMJ'),
('197910062003122001', 'Prihatin Oktivasari', '$2y$10$6.etP330nnzRMDRM94sVjeWyUK0/O6EBrari5VKO3Br33aC00sdpO', 'TMJ'),
('198112012015041001', 'Defiana Arnaldy', '$2y$10$DUqDq.05IjgDEmf.Z2rZW.8yZgGvVIJkStsr6VnqH09vvWRYVXQaC', 'TMJ'),
('198501292010121003', 'Ariawan Andi Suhandana', '$2y$10$lpdw1kfl7yr47uv1GrCkLO.faGLROIxdpuo31LvJFnqtfgKGTlPwO', 'TMJ'),
('198605222023212032', 'Susana Dwi Yulianti', '$2y$10$1jq5AkZJBLMt4JlRaoJKeeb8cB/XKPmLTsY4Cb46SkmFsSG63oiYS', 'TMJ'),
('198910112018032002', 'Ayu Rosyida Zain', '$2y$10$KdJA62ySgWEADuPg9G7IpO0AWcgc2QjRG3E90j2xribZZLq.IsbeK', 'TMJ'),
('199109262019031012', 'Asep Kurniawan', '$2y$10$eDDlp8qcdav6FfF.6.IZt.n/avf./4MNczJr/vmLskhfgIWU42Bvi', 'TMJ'),
('199206052022032008', 'Ratna Widya Iswara', '$2y$10$GMerD64r8dptIBdKsyFU6.rf54zpZstla.7ayLIryl6e6rdjFHEL6', 'TMJ'),
('199408202022031009', 'Iik Muhamad Malik Matin', '$2y$10$Qpb3Ar/0VIfbm210h7fYyelC2cX0DlxscUMG8dO/1i9fXzqAA9DYy', 'TMJ');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_kelas`
--

CREATE TABLE `tbl_kelas` (
  `kelas` varchar(10) NOT NULL COMMENT 'Kelas Mahasiswa/i',
  `jurusan` enum('TIK','TGP','TE','TS') NOT NULL COMMENT 'Jurusan Mahasiswa/i',
  `prodi` enum('TI','TMD','TMJ','TKJ','TICK') NOT NULL COMMENT 'Prodi Mahasiswa/i',
  `smt` int(2) NOT NULL COMMENT 'Semester Mahasiswa/i'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabel Kelas';

--
-- Dumping data for table `tbl_kelas`
--

INSERT INTO `tbl_kelas` (`kelas`, `jurusan`, `prodi`, `smt`) VALUES
('TI-3A', 'TIK', 'TI', 3),
('TI-3B', 'TIK', 'TI', 3),
('TMJ-2A', 'TIK', 'TMJ', 2),
('TMJ-2B', 'TIK', 'TMJ', 2),
('TMJ-3A', 'TIK', 'TMJ', 3),
('TMJ-3B', 'TIK', 'TMJ', 3);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_mhsw`
--

CREATE TABLE `tbl_mhsw` (
  `NIM` varchar(10) NOT NULL COMMENT 'NIM Mahasiswa',
  `nama_mhsw` varchar(70) NOT NULL COMMENT 'Nama mahasiswa (akun)',
  `password` varchar(255) NOT NULL COMMENT 'Password akun website absensi',
  `uid` varchar(20) NOT NULL COMMENT 'UID Mahasiswa/i',
  `kelas` varchar(10) NOT NULL COMMENT 'Kelas dari mahasiswa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_mhsw`
--

INSERT INTO `tbl_mhsw` (`NIM`, `nama_mhsw`, `password`, `uid`, `kelas`) VALUES
('2207421031', 'Muhammad Khairu Mufid', '$2y$10$BNO9vzJVOFwQnblpD0KXi.sH1eB9A/O0OzPlIslVvGrVYfxcfnnLC', '2111593213400', 'TMJ-3B'),
('2207421032', 'Kevin Alonzo Manuel Bakara', '$2y$10$nlsq6jJCk7E6T2dL5I8trOyK6hof.UIEaT1VXN4O0orv0Ff.kzxl2', '914183163', 'TMJ-3B'),
('2207421046', 'Abdurrahman Ammar Ihsan', '$2y$10$Laxvc0s8gtEhdg.f1e3pMu9S./QjlB.jh4uz1cYHyNZH9DpDYY41C', '4604434244106128', 'TMJ-3B'),
('2207421048', 'Wahyu Priambodo', '$2y$10$iEhP/7vkBRGTIStUr6KBb.Hd.Kx7tCy3dt9ZM40ifPvhST8xsU8I.', '416502265111128', 'TMJ-3B'),
('2207421056', 'Shaquille Arriza Hidayat', '$2y$10$u64cyg7wk7ZEdRKi3HoWfumjhXNS7Uw74rG/0FgshXyEOoSTi5UMm', '51208229182', 'TMJ-3B'),
('2207421057', 'Muhammad Brian Azura Nixon', '$2y$10$NaNTYBWgc7xJeG.UKhOMueUwn45QapLiXWvjzItVtf5ikqoUBSyUK', '2531321684640', 'TMJ-3B'),
('2207421059', 'Cornelius Yuli Rosdianto', '$2y$10$QiYUBsP0P9s/ZteNJnAsGeS5I.0rJloGfcxt86bApx.cLFeAVmCAa', '1234', 'TMJ-3B');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_absen`
--
ALTER TABLE `tbl_absen`
  ADD PRIMARY KEY (`hari_tanggal`),
  ADD KEY `tbl_absen_FK` (`NIM`),
  ADD KEY `id_matkul` (`id_matkul`);

--
-- Indexes for table `tbl_admin`
--
ALTER TABLE `tbl_admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `tbl_course`
--
ALTER TABLE `tbl_course`
  ADD PRIMARY KEY (`id_matkul`),
  ADD KEY `NIP` (`NIP`),
  ADD KEY `kelas` (`kelas`);

--
-- Indexes for table `tbl_dosen`
--
ALTER TABLE `tbl_dosen`
  ADD PRIMARY KEY (`NIP`);

--
-- Indexes for table `tbl_kelas`
--
ALTER TABLE `tbl_kelas`
  ADD PRIMARY KEY (`kelas`);

--
-- Indexes for table `tbl_mhsw`
--
ALTER TABLE `tbl_mhsw`
  ADD PRIMARY KEY (`NIM`),
  ADD KEY `kelas` (`kelas`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_absen`
--
ALTER TABLE `tbl_absen`
  ADD CONSTRAINT `tbl_absen_FK` FOREIGN KEY (`NIM`) REFERENCES `tbl_mhsw` (`NIM`),
  ADD CONSTRAINT `tbl_absen_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `tbl_course` (`id_matkul`);

--
-- Constraints for table `tbl_course`
--
ALTER TABLE `tbl_course`
  ADD CONSTRAINT `tbl_course_ibfk_1` FOREIGN KEY (`NIP`) REFERENCES `tbl_dosen` (`NIP`),
  ADD CONSTRAINT `tbl_course_ibfk_2` FOREIGN KEY (`kelas`) REFERENCES `tbl_kelas` (`kelas`);

--
-- Constraints for table `tbl_mhsw`
--
ALTER TABLE `tbl_mhsw`
  ADD CONSTRAINT `tbl_mhsw_ibfk_1` FOREIGN KEY (`kelas`) REFERENCES `tbl_kelas` (`kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
