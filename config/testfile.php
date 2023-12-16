<?php

setlocale(LC_TIME, 'id_ID');
date_default_timezone_set('Asia/Jakarta');

require __DIR__.'/functions.php';
$mqtt_client->presence();
// echo $mqtt_client->presence();
// echo $mqtt_client->send_message("test123");
// $current_date = date('D');
// switch ($current_date) {
//   case 'Mon':
//     $current_date = "Senin";
//     break;
//   case 'Tue':
//     $current_date = "Selasa";
//     break;
//   case 'Wed':
//     $current_date = "Rabu";
//     break;
//   case 'Thu':
//     $current_date = "Kamis";
//     break;
//   case 'Fri':
//     $current_date = "Jumat";
//     break;
//   case 'Sat':
//     $current_date = "Sabtu";
//     break;
//   case 'Sun':
//     $current_date = "Minggu";
//     break;
//   default:
//     $current_date = "Days not found";
//     break;
// }

// $student_class = $db_functions->get_student_data_by_uid('167907098')['kelas'];
// $student_nim = $db_functions->get_student_data_by_uid('167907098')['NIM'];
// $all_courses = $db_functions->get_all_student_courses($student_class);
// $status = "";
// $course_id = "";
// $found = false;
// $current_time = strtotime(date('H:i:s'));

// foreach ($all_courses as $course) {
//   if ( $course['hari'] === $current_date ) {
//     $start_time = strtotime($course['jam_mulai']);
//     $end_time   = strtotime($course['jam_selesai']);

//     // jika mahasiswa hadir tepat waktu
//     if ( $current_time >= $start_time && $current_time <= $start_time + (10 * 60) ) {
//       $found      = true;
//       $course_id = $course['id_matkul'];
//       $status     = "Hadir";
//       break;
//     }
//     // jika mahasiswa terlambat 10 menit
//     else if ( $current_time > $start_time + (10 * 60) && $current_time <= $end_time ) {
//       $found      = true;
//       $status     = "Terlambat";
//       $course_id = $course['id_matkul'];
//       break;
//     }
//     // jika mahasiswa tidak hadir / alpa
//     else if ( $current_time > $end_time ) {
//       $found      = true;
//       $status     = "Alpa";
//       $course_id = $course['id_matkul'];
//       break;
//     }
//   }
  
//   // $course_id = $course['id_matkul'];
//   // echo $course['jam_mulai'] . "<br>";
//   // echo $course['jam_selesai'] . "<br>";
//   // echo $course['hari'] . "<br>";
//   // echo $course['id_matkul'] . "<br>";
// }

// if ( $found ) {
//   echo $status . "<br>";
//   $current_datetime = new DateTime();
//   $formatted_current_datetime = $current_datetime->format('Y-m-d H:i:s');

//   $formatted_current_time = date("H:i:s", $current_time);

//   $db_functions->add_student_attendance($formatted_current_datetime, $formatted_current_time, $student_nim, $course_id, $status);
//   echo "Data berhasil ditambahkan";

//   $message = [
//     "keterangan" => "Student UID is registered",
//     "status" => $status,
//   ];
//   // publish the message in json format
//   $mqtt_client->publish($pub_topic, json_encode($message), 0);
// } else {
//   echo $status . "<br>";
// }

// $student_class = $db_functions->get_student_data_by_uid('1234');
// echo $student_class['kelas'];
// $student_nim     = $db_functions->get_student_data_by_uid($uid);
// $student_courses = $db_functions->get_all_student_courses($student_class);

//         $found        = false; // penanda jika mahasiswa memiliki jadwal saat ini
//         $course_id    = null;
//         $status       = null; 

//         foreach ( $student_courses as $course ) {
//           // cek apakah hari ini ada jadwal
//           if ( $course['hari'] !== $current_date ) {
//             break;
//           }

//           $start_time = strtotime($course['jam_mulai']);
//           $end_time   = strtotime($course['jam_selesai']);

//           // jika mahasiswa hadir tepat waktu
//           if ( $current_time >= $start_time && $current_time <= $start_time + (10 * 60) ) {
//             $found      = true;
//             $course_id  = $course['id_matkul'];
//             $status     = "Hadir";
//             break;
//           }
//           // jika mahasiswa terlambat 10 menit
//           else if ( $current_time > $start_time + (10 * 60) && $current_time <= $end_time ) {
//             $found      = true;
//             $course_id  = $course['id_matkul'];
//             $status     = "Terlambat";
//             break;
//           }
//           // jika mahasiswa tidak hadir / alpa
//           else if ( $current_time > $end_time ) {
//             $found      = true;
//             $course_id  = $course['id_matkul'];
//             $status     = "Alpa";
//             break;
//           }
//         }

?>