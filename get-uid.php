<!DOCTYPE html>
<html>
<head>
    <title>Tampilkan UID</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript">
    	$(document).ready(function() {
            // Memuat data uid saat halaman dimuat
            loadDataUid();
            // Memuat data uid setiap detik
            setInterval(loadDataUid, 0);
        });

        function loadDataUid() {
            $("#dataUid").load("read-uid.php", function(response, status, xhr) {
                if (status == "success") {
                    // Mengubah value dari input dataUid dengan data uid yang sesungguhnya
                    $("#dataUid").val(response);
                } else {
                    // Tindakan jika gagal memuat data
                    console.log("Gagal memuat data");
                }
            });
        }
    </script>

</head>
<body>
    <h1>Data UID yang Diterima:</h1>
    <input type="text" name="dataUid" id="dataUid" value="" />
</body>
</html>
