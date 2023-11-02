-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 02, 2023 at 06:15 PM
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
-- Database: `Coba`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_admin`
--

CREATE TABLE `tbl_admin` (
  `id_admin` varchar(5) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `jurusan` enum('TIK','TGP','TS') NOT NULL,
  `no_telp` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabel Admin';

--
-- Dumping data for table `tbl_admin`
--

INSERT INTO `tbl_admin` (`id_admin`, `password`, `nama`, `jurusan`, `no_telp`) VALUES
('1234', '$2y$10$M06Gs22NzPyJNYT1SweE5.o0.55RR3QtiVlf9/huDiGYdcvbhLXWy', 'Admin 1', 'TIK', ''),
('2345', '$2y$10$39GYenAtPd7QIo6S4Wi2beRRqrXSuvs7TrZxOV5CBj0X5KaHJ4226', 'Admin 2', 'TGP', ''),
('3456', '$2y$10$tI0TV2EUvZK5LsUWhE5Xu.ZeGY5Rqyyyh5bCmlSpQYuisFYNSQ3.m', 'Admin 3', 'TS', '');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_dosen`
--

CREATE TABLE `tbl_dosen` (
  `nip` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `no_telp` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabel Dosen';

--
-- Dumping data for table `tbl_dosen`
--

INSERT INTO `tbl_dosen` (`nip`, `password`, `nama`, `email`, `no_telp`) VALUES
('12345', '$2y$10$9lxoRuqg/AqeCYMloN4/yuj/yLqqmxVZuyZhx.vD6ahPvGn5P/Zvi', 'Iik Muhammad Malik Matin', 'iik.muhammad.malik.matin@dosen.pnj.ac.id', NULL),
('123456', '$2y$10$/ZKk2nnQEbxodOag/QXq2O2HAR6DD8X.pqHEaO2uGp8bWYJeLDaxu', 'Maria Agustin', 'maria.agustin@dosen.pnj.ac.id', NULL),
('1234567', '$2y$10$tMJ4TUkhzwein6S1kxJr8uScgBk.5Y3oN1yCG3VY5kmcAeOYLvSlK', 'Ariawan Andi Suhandana', 'ariawan.andi.suhandana@dosen.pnj.ac.id', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_mhsw`
--

CREATE TABLE `tbl_mhsw` (
  `nim` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `uid` varchar(20) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `kelas` enum('TMJ-3B','TMJ-3A') NOT NULL,
  `no_telp` varchar(13) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabel Mahasiswa/i';

--
-- Dumping data for table `tbl_mhsw`
--

INSERT INTO `tbl_mhsw` (`nim`, `password`, `uid`, `nama`, `kelas`, `no_telp`) VALUES
('2207421031', '$2y$10$slr55dgKg9FxPd1JG08SluZ.EoHh6SbCjj/jag/lpA8DrlrcpPkvy', '167907098', 'Muhammad Khairu Mufid', 'TMJ-3B', NULL),
('2207421032', '$2y$10$bxiatjdeHBU/fbMXOGqtCOUkCyxQq0nT4HFspA8AvXYft3XZ/kTjG', '914183163', 'Kevin Alonzo Manuel Bakara', 'TMJ-3B', NULL),
('2207421048', '$2y$10$ywwub5YTu/f08dJni1l4feAi4Hxrdoep3kDD0bAu5I91CQBsb7XTi', '167907098', 'Wahyu Priambodo', 'TMJ-3B', NULL),
('2207421056', '$2y$10$Y9BAvm3goG.jWthXcatoueFSFZlt3eN6B832Ljf.q7rS1ehqW1U2C', '914183163', 'Muhammad Brian Azura Nixon', 'TMJ-3B', NULL),
('2207421057', '$2y$10$tKKTKOeJFodhqDNd8WeWbubHGszrFgg1VPVeDAtPL/fCcJh/dNbmO', '167907098', 'Shaquille Arriza Hidayat', 'TMJ-3B', NULL),
('2207421059', '$2y$10$6xv8Lf9par8ojjvdczgaTumZRbiHXZII.UphFN1z7l14pdIISnlwG', '914183163', 'Cornelius Yuli Rosdianto', 'TMJ-3B', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_admin`
--
ALTER TABLE `tbl_admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `tbl_dosen`
--
ALTER TABLE `tbl_dosen`
  ADD PRIMARY KEY (`nip`);

--
-- Indexes for table `tbl_mhsw`
--
ALTER TABLE `tbl_mhsw`
  ADD PRIMARY KEY (`nim`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
