-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 13, 2024 at 01:35 PM
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
-- Database: `smartendance-v2`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('97a5116b3148');

-- --------------------------------------------------------

--
-- Table structure for table `class`
--

CREATE TABLE `class` (
  `class_id` char(10) NOT NULL,
  `class_study_program` enum('TMJ','TMD','TI','TKJ') NOT NULL,
  `class_major` enum('TIK','TE','TGP','TM','TS') NOT NULL,
  `class_description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `class`
--

INSERT INTO `class` (`class_id`, `class_study_program`, `class_major`, `class_description`) VALUES
('TMJ-3A', 'TMJ', 'TIK', NULL),
('TMJ-3B', 'TMJ', 'TIK', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_id` char(15) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `course_sks` int(11) NOT NULL,
  `at_semester` int(11) NOT NULL,
  `day` varchar(9) NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL,
  `course_description` text DEFAULT NULL,
  `lecturer_nip` varchar(18) NOT NULL,
  `class_id` char(10) NOT NULL,
  `room_id` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lecturer_attendance_logs`
--

CREATE TABLE `lecturer_attendance_logs` (
  `log_id` int(11) NOT NULL,
  `time_in` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('PRESENT','LATE','ALPHA') NOT NULL,
  `lecturer_nip` varchar(18) NOT NULL,
  `course_id` char(15) NOT NULL,
  `room_id` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `room_id` varchar(10) NOT NULL,
  `room_building` enum('GSG','AA') NOT NULL,
  `room_description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`room_id`, `room_building`, `room_description`) VALUES
('AA204', 'AA', NULL),
('GSG210', 'GSG', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `student_attendance_logs`
--

CREATE TABLE `student_attendance_logs` (
  `log_id` int(11) NOT NULL,
  `time_in` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('PRESENT','LATE','ALPHA') NOT NULL,
  `student_nim` varchar(18) NOT NULL,
  `course_id` char(15) NOT NULL,
  `room_id` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` varchar(18) NOT NULL,
  `user_role` enum('ADMIN','LECTURER','STUDENT') NOT NULL,
  `user_fullname` varchar(200) NOT NULL,
  `user_password_hash` varchar(256) NOT NULL,
  `user_rfid_hash` varchar(256) DEFAULT NULL,
  `user_email_address` varchar(100) NOT NULL,
  `user_home_address` varchar(256) DEFAULT NULL,
  `lecturer_major` enum('TIK','TE','TGP','TM','TS') DEFAULT NULL,
  `student_class` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `user_role`, `user_fullname`, `user_password_hash`, `user_rfid_hash`, `user_email_address`, `user_home_address`, `lecturer_major`, `student_class`) VALUES
('1234567890', 'ADMIN', 'Admin Satu', '$argon2id$v=19$m=65536,t=3,p=4$/NVHzuosbajWfAcrWiv+kg$afqhI0LRGJOGnL7/wJ2RzGWbz/3F/8+mUieQaCvbzwE', NULL, 'admin1@tik.pnj.ac.id', NULL, NULL, NULL),
('197509152003122003', 'LECTURER', 'Maria Agustin', '$argon2id$v=19$m=65536,t=3,p=4$ssO7Dv0WIm3/Y5RNFsRdPg$H5SDId/KdDEnccPbojyW67HbMLrk1vbLlGDtFDzUYbQ', '$argon2id$v=19$m=65536,t=3,p=4$D9TTejpOGLHveQKtRtcPyg$9kwGOgacBeJJSDO6wZZWOCSnZuQbuTKYK7yyJfxIjDA', 'maria.agustin@tik.pnj.ac.id', NULL, 'TIK', NULL),
('197910062003122001', 'LECTURER', 'Prihatin Oktivasari', '$argon2id$v=19$m=65536,t=3,p=4$mCP2f/ZXJNu7Qkzvux/zKw$3sE/H6SNKCfZTeegg48Oqpg1+vZp8HrxwQEz8JJ7NEc', '$argon2id$v=19$m=65536,t=3,p=4$LODXTu4Q+1Ws2t1sKkjtvw$jGavj3XkeM/2I+9YqIVRSYFpnG9zQ/l0erueHeKFsvo', 'prihatin.oktivasari@tik.pnj.ac.id', NULL, 'TIK', NULL),
('198112012015041001', 'LECTURER', 'Defiana Arnaldy', '$argon2id$v=19$m=65536,t=3,p=4$2PUg2Kr/10shESpi+hTHQw$5RrxFO+m+2H04AqthOvXwFuKbV5RKrxMlv2nQQzYo6w', '$argon2id$v=19$m=65536,t=3,p=4$sfCMfRN5BlpaueQIQg8U/w$0OGO4enpnLYbc0gacDO1+5FhmD6Q5Pd6j+uC+vA+gu4', 'defiana.arnaldy@tik.pnj.ac.id', NULL, 'TIK', NULL),
('198501292010121003', 'LECTURER', 'Ariawan Andi Suhandana', '$argon2id$v=19$m=65536,t=3,p=4$1etgUc0HcAtgsMjuUysZqg$94Y1tSgl4WTBUcmGCK6/E5jVNVQGmTeRkTcmGtMl3zg', '$argon2id$v=19$m=65536,t=3,p=4$N+nUXYJ+etgYZnWwg0E+zw$HjTSbwfSiVZn2OQw/39S4h9neJY2bx7ofqiWBJV6igE', 'ariawan.andi.suhandana@tik.pnj.ac.id', NULL, 'TIK', NULL),
('198605222023212032', 'LECTURER', 'Susana Dwi Yulianti', '$argon2id$v=19$m=65536,t=3,p=4$on3Mb/aNBuBejfi5N4fZ4A$H2Hmf1HyeBDS2TRiXYGctk2/ZvKkQfkKwi7D9FDyckM', '$argon2id$v=19$m=65536,t=3,p=4$UWjG5AXQQTLn8q3LnyMxKQ$cYEeswxLMoZEFdYZja+iDEvduWl0jwQvKde4gISJOmo', 'susana.dwiyulianti@tik.pnj.ac.id', NULL, 'TIK', NULL),
('198910112018032002', 'LECTURER', 'Ayu Rosyida Zain', '$argon2id$v=19$m=65536,t=3,p=4$mEq/jVbk/vComXCMaSL9+w$/o4O0/qJaa3kXAaQcGb79ujoNhS9as6xAnItx8s3hFs', '$argon2id$v=19$m=65536,t=3,p=4$y7tJe/qvs5i88ZzehAGheg$DfdvzcIqXnvJ72EPrR6O8mYaBrbxblIDGjM72IE38b0', 'ayu.rosyidazain@tik.pnj.ac.id', NULL, 'TIK', NULL),
('199109262019031012', 'LECTURER', 'Asep Kurniawan', '$argon2id$v=19$m=65536,t=3,p=4$m4FRK+CV3rAiuQBzMedoQQ$S/hlkIwFnUJLhZfwzCeY/u5to+8T5gkiXWJkQW4TNYI', '$argon2id$v=19$m=65536,t=3,p=4$04V/+gRCIVbAKEYrPa83Rw$TRtH/7IOesUG5NOdE5qpXelillNN3LdAKFiuadFdSGI', 'asep.kurniawan@tik.pnj.ac.id', NULL, 'TIK', NULL),
('199206052022032008', 'LECTURER', 'Ratna Widya Iswara', '$argon2id$v=19$m=65536,t=3,p=4$AiccjdDQaJ45DBwu3qPBpw$XCKv3pm67q89vAziRRQN6WoXIjW999vTqrRz4vxtt6Q', '$argon2id$v=19$m=65536,t=3,p=4$xjJ/JW/++hPjf0mIhYKI3g$8MjaOgSKJpDVp2G/7J1jLeB1pLVkG5/n482RSpY0REs', 'ratna.widya.iswara@tik.pnj.ac.id', NULL, 'TIK', NULL),
('199408202022031009', 'LECTURER', 'Iik Muhamad Malik Matin', '$argon2id$v=19$m=65536,t=3,p=4$y78B+oyVIl9QAYXCOOwp/A$AC/xH9xuKb2G4O896gEM1lLU8/peF007FzYbsmEcqfc', '$argon2id$v=19$m=65536,t=3,p=4$Kcumo0XQMRxHyVjJjcBh8Q$6iQhdRrQ80kAlRFHujRjD6tNLJB4jGmo8WW74TdzYXE', 'iik.muhamad.malik.matin@tik.pnj.ac.id', NULL, 'TIK', NULL),
('2207421031', 'STUDENT', 'Muhammad Khairu Mufid', '$argon2id$v=19$m=65536,t=3,p=4$M4/Uhl73xK8tluGqpJE0UQ$hcSLDrk6m4rTE4Sqijcz4i3Ln7gDnWg/vqZzfNhHozc', '$argon2id$v=19$m=65536,t=3,p=4$2uvEgbOjUriRVaOTJgJhrA$/oL5ZSOg1JZgHryGV6T2ltct+m9EDVF7BqHwMEdcRpQ', 'muhammad.khairu.mufid.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421032', 'STUDENT', 'Kevin Alonzo Manuel Bakara', '$argon2id$v=19$m=65536,t=3,p=4$xI/30BK3vcUWqEjTxxYPlA$AAUlYoIL1WAP/2PTgTnVDinb7S+RZFRMcy6nt1RUmqI', '$argon2id$v=19$m=65536,t=3,p=4$WoG9Zo0/Ei1JPkrWOSWS9w$+iNBvfSs7r2E+Lr9HIDZjVsgPhKaK2oBaD8lN6N5LCc', 'kevin.alonzo.manuel.bakara.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421033', 'STUDENT', 'Devina Anggraini', '$argon2id$v=19$m=65536,t=3,p=4$MeUyzX+cmpu29ahcSd13uw$gKBRAWDLVCrvqNs/4BfQmXgjHA8TThE3UIpcHR90f2g', '$argon2id$v=19$m=65536,t=3,p=4$hx8NWi+9JZZ8hBwnHDe6ig$VuTi/MjBDfGOrZc2KMZh8FCqc5R/v2Nrtcqld1cV7PU', 'devina.anggraini.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421034', 'STUDENT', 'Alif Rendina Pamungkas', '$argon2id$v=19$m=65536,t=3,p=4$sUvXOSCu0z6CaHJcb1eo5w$gduQsF5APel878L+DDTfKsD/YsE/whgbDDZz8uN7LIg', '$argon2id$v=19$m=65536,t=3,p=4$WYfUKEeUwoVWdt86QFwBaQ$xNoKt9CTlaZaEr+Hq12iKYPglg5aFihJ9Ud9X++e4Nw', 'alif.rendina.pamungkas.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421035', 'STUDENT', 'Ibrahim Alvaro', '$argon2id$v=19$m=65536,t=3,p=4$sIpl4fXTMLxcAwOolJgBPQ$l/xChySkOjL3x569fqqVcFMNwKWafNJ3QDRskVKBGX0', '$argon2id$v=19$m=65536,t=3,p=4$BbElZQJNiIQoV4do0lqO2g$bMNHcETxDUTMJlbo90azVn3vGs9Ga9rabrlpqmxjTDU', 'ibrahim.alvaro.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421047', 'STUDENT', 'Abdurrahman Ammar Ihsan', '$argon2id$v=19$m=65536,t=3,p=4$EwB4tzes72AfYndnT8uYLA$2BcT1aCeZ62G3h1OCiNh19Ku1Pc5OYpN2VhsV4C+lVU', '$argon2id$v=19$m=65536,t=3,p=4$RmuOg/qk+BCRuWjFVlS4SQ$/zNvVQ5ZDwZQeNrp7SLWSfehvE4VZHcatjkj9/dtvKE', 'abdurrahman.ammar.ihsan.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421048', 'ADMIN', 'Wahyu Priambodo', '$argon2id$v=19$m=65536,t=3,p=4$Loo/a50SSz2jKbxXwSCy/g$KKGaABgdeRe0habVBr3GHrhyzxs49J3U3uDfBEBFArw', NULL, 'wahyu.priambodo.tik22@mhsw.pnj.ac.id', NULL, NULL, NULL),
('2207421049', 'STUDENT', 'Salsabila Aulia', '$argon2id$v=19$m=65536,t=3,p=4$IKqSDcXBACgQHPBsQb8RZQ$iHAJlO0nDmmlquGI2Xh9Jipngz3LK0IbURBcAU3gYbU', '$argon2id$v=19$m=65536,t=3,p=4$s6QQZv+vHZ5FsqhG5yfEWA$Mf4sF/Yn2fs2id2qD6H8H4ZwClQk2qj3xz0fy5CPiBM', 'salsabila.aulia.tik22@mhsw.pnj.ac.id', 'Test.', NULL, 'TMJ-3B'),
('2207421056', 'STUDENT', 'Muhammad Brian Azura Nixon', '$argon2id$v=19$m=65536,t=3,p=4$NijZ400iDOzAFcrthn543Q$Fd7o94RdGjuHyHL5PK/hV8Z7Ydm6T5SSQ5IvxnX/ATA', '$argon2id$v=19$m=65536,t=3,p=4$98jNpsMJKriWagOif9g5JA$UusgRzziBXo55kwo/mhnUs+M4lBc4NI+yOfI1/D5JOQ', 'muhammad.brian.azura.nixon.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421057', 'STUDENT', 'Shaquille Arriza Hidayat', '$argon2id$v=19$m=65536,t=3,p=4$x9gutpgd4xseDPAAkGruWg$rIQbuIN7dy81rx9l+xNDM10Fi9K1MBlmoH7x+lw6HWw', '$argon2id$v=19$m=65536,t=3,p=4$9HqMjp/5GRbV6JAajPMDEA$mGE5oDISGUc2F2hn1TTbXm14MqtAc8FloAcjVrazGRg', 'shaquille.arriza.hidayat.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B'),
('2207421059', 'STUDENT', 'Cornelius Yuli Rosdianto', '$argon2id$v=19$m=65536,t=3,p=4$OyvSt33WArCGKAdKxlrtfA$UrMxvFOJoUALfydCnYXLKhaYa7rdQYhGBv1UGFUH0hI', '$argon2id$v=19$m=65536,t=3,p=4$aSmM2ttUvAosgiy7I5dt+g$DWOFdlIYCjXEkk+2jYviC4rN4HuXMvhKyzqtQveENZU', 'cornelius.yuli.rosdianto.tik22@mhsw.pnj.ac.id', NULL, NULL, 'TMJ-3B');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `class`
--
ALTER TABLE `class`
  ADD PRIMARY KEY (`class_id`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`),
  ADD UNIQUE KEY `course_name` (`course_name`),
  ADD KEY `class_id` (`class_id`),
  ADD KEY `lecturer_nip` (`lecturer_nip`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `lecturer_attendance_logs`
--
ALTER TABLE `lecturer_attendance_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `lecturer_nip` (`lecturer_nip`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`room_id`);

--
-- Indexes for table `student_attendance_logs`
--
ALTER TABLE `student_attendance_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `room_id` (`room_id`),
  ADD KEY `student_nim` (`student_nim`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email_address` (`user_email_address`),
  ADD UNIQUE KEY `user_rfid_hash` (`user_rfid_hash`),
  ADD KEY `student_class` (`student_class`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `lecturer_attendance_logs`
--
ALTER TABLE `lecturer_attendance_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_attendance_logs`
--
ALTER TABLE `student_attendance_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`),
  ADD CONSTRAINT `course_ibfk_2` FOREIGN KEY (`lecturer_nip`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `course_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`);

--
-- Constraints for table `lecturer_attendance_logs`
--
ALTER TABLE `lecturer_attendance_logs`
  ADD CONSTRAINT `lecturer_attendance_logs_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  ADD CONSTRAINT `lecturer_attendance_logs_ibfk_2` FOREIGN KEY (`lecturer_nip`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `lecturer_attendance_logs_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`);

--
-- Constraints for table `student_attendance_logs`
--
ALTER TABLE `student_attendance_logs`
  ADD CONSTRAINT `student_attendance_logs_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  ADD CONSTRAINT `student_attendance_logs_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`),
  ADD CONSTRAINT `student_attendance_logs_ibfk_3` FOREIGN KEY (`student_nim`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`student_class`) REFERENCES `class` (`class_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
