<div align="center">
   <h1>IoT-Attendance-System (Under Development)</h1>
   <img src="https://media.giphy.com/media/7NoNw4pMNTvgc/giphy.gif" width="300" height="300" alt="On Progress!"/>
   </br>
   <img src="https://img.shields.io/badge/release-under_development-FC929E"/>
   <img src="https://img.shields.io/github/contributors/wahyu-priambodo/IoT-Attendance-System"/>
   <img src="https://img.shields.io/github/stars/wahyu-priambodo/IoT-Attendance-System"/>
</div>
</br>

<div align="center">
  { <a href="#about">About</a> |
  <a href="#planning">Planning</a> |
  <a href="#requirements">Requirements</a> |
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> |
  <a href="#contributors">Contributors</a> }
</div>
</br>

# About
<p><strong>IoT Attendance System</strong> yang sedang kami kembangkan adalah solusi modern untuk mengelola kehadiran mahasiswa di lingkungan perkuliahan. Sistem ini dirancang untuk memudahkan proses absensi dan meningkatkan efisiensi dalam merekapitulasi absensi mahasiswa. Sistem ini nantinya akan mengintegrasikan perangkat-perangkat IoT dengan  aplikasi berbasis web dan aplikasi berbasis mobile, yang memungkinkan mahasiswa untuk melakukan absensi dengan mudah dan cepat.</p>

# Planning
<p>Beberapa target yang akan kami kembangkan lagi ke depannya antara lain:</p>
<ul>
   <li><strong>Peningkatan keamanan (Security Enhancement)</strong>
      <ul>
         <li>Menggunakan sensor fingerprint dan pin (numpad)</li>
         <li>Autentikasinya berbasis JWT + dienkripsi menggunakan XOR</li>
      </ul>
   </li>
   <li>Penambahan fitur:
      <ul>
         <li>Memunculkan notifikasi ke gmail setiap mahasiswa setelah melakukan absensi</li>
         <li>Menyediakan statistik kehadiran mahasiswa untuk dosen/lecturer</li>
         <li>Export to PDF/Excel dengan template yang telah di-generate</li>
      </ul>
   </li>
</ul>

# Requirements
## Hardware:
<ul>
   <li>Arduino Uno R3</li>
   <li>NodeMCU ESP8266</li>
   <li>RFID sensor (MFRC522)</li>
   <li>Identity card like <strong>e-KTP/SIM</strong> as RFID card</li>
   <li>Buzzer</li>
   <li>LCD 16x2 I2C</li>
   <li>Mini buzzer</li>
   <li>Fingerprint sensor <em>(futher work)</em></li>
   <li>Jumper cable <strong>(male to male & male to female)</strong></li>
   <li>Adaptor 5V</li>
</ul>

## Softwares:
<ul>
   <li>Python 3 <strong>ver-3.10.12</strong> or above</li>
   <li>Flask framework <strong>ver-3.0.0</strong> (Backend)</li>
   <li>MySQL server & client <strong>ver-8.0.34</strong> (Database)</li>
   <li>phpMyAdmin for managing MySQL databases</li>
   <li>Git</li>
   <li>Arduino IDE</li>
   <li>Visual Studio Code</li>
   <li>Web Browser, we recommend to use <strong>Google Chrome/Mozilla Firefox</strong> for compatibility reason</li>
   <li>...</li>
</ul>

# Installation
<p>Soon...</p>

# Usage
<p>Soon... You can visit our wiki for the details at <strong>bla bla bla</strong>...</p>

# Contributors
## Members of the 3rd group include:
<ul>
   <li>Muhammad Khairu Mufid (2207421031)</li>
   <li>Kevin Alonzo Manuel Bakara (2207421032)</li>
   <li>Wahyu Priambodo (2207421048)</li>
   <li>Muhammad Brian Azura Nixon (2207421056)</li>
   <li>Shaquille Ariza Hidayat (2207421057)</li>
   <li>Cornelius Yuli Rosdianto (2207421059)</li>
</ul>

# Todos
- [X] Making a **block diagram** and **simple flowchart**
<div align="center">
   <img src="https://github.com/wahyu-priambodo/RFID-Attendance-System/assets/78311798/6054ecb4-650b-4130-992a-01184a24ad63" alt="block-diagram" width="100%">
   <p>Image 1. Block Diagram</p>
   <hr>
   <img src="https://github.com/wahyu-priambodo/RFID-Attendance-System/assets/78311798/685e0448-2d1e-4595-af2a-1fb64be1ed16" alt="flowchart" width="30%">
   <p>Image 2. Flowchart</p>
</div>
<hr>

- [X] **Project Requirements**: https://docs.google.com/document/d/1HgZa5Btvx8v64lG_GeFaTAc-W5RzYUj6E80HYkERNlI/edit?usp=sharing
- [ ] **Connecting Flask to MySQL Db**

<br><br>

<footer>
   <p align="right">Copyright &copy;2023 Developed by 3rd Group</p>
</footer>
