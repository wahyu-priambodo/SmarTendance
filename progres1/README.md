# Konektivitas sensor RFID RC522 dengan NodeMCU ESP8266 12E

<p>Hubungan antara pin-pinnya adalah sebagai berikut:</p>
<div align="center">
  <table border="1">
    <tr>
      <th>RC522</th>
      <th>ESP8266</th>
    </tr>
    <tr>
      <td>RST</td>
      <td>D1</td>
    </tr>
    <tr>
      <td>SDA</td>
      <td>D2</td>
    </tr>
    <tr>
      <td>SCK</td>
      <td>D5</td>
    </tr>
    <tr>
      <td>MISO</td>
      <td>D6</td>
    </tr>
    <tr>
      <td>MOSI</td>
      <td>D7</td>
    </tr>
  </table>
</div>

<p>
  Status Progres: <strong>Sukses</strong>
  <br>

  Referensi: <a href="https://medium.com/@muftiramdhani25/rfid-with-nodemcu-9786ee786101">https://medium.com/@muftiramdhani25/rfid-with-nodemcu-9786ee786101</a>
</p>

<p>Dependensi:</p>
<ul>
  <li><strong>Library</strong>: MFRC522 versi ^1.4.10 by GithubCommunity</li>
  <li><strong>Board</strong>: esp8266 versi 3.1.2 by ESP8266 Community</li>
</ul>