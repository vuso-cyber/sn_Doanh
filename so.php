// File: save_greeting.php
header('Content-Type: application/json; charset=utf-8');

// Cấu hình DB
define('DB_HOST','127.0.0.1');
define('DB_NAME','birthday');
define('DB_USER','root');
define('DB_PASS','password_here');

$input = json_decode(file_get_contents('php://input'), true);
$to = $input['to'] ?? 'Doanh';
$from = $input['from'] ?? 'Bạn';
$message = $input['message'] ?? '';

try {
    $pdo = new PDO("mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4", DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
    $stmt = $pdo->prepare("INSERT INTO greetings (recipient, sender, message, created_at) VALUES (:r,:s,:m,NOW())");
    $stmt->execute([':r'=>$to, ':s'=>$from, ':m'=>$message]);
    echo json_encode(['status'=>'ok']);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['status'=>'error','msg'=>$e->getMessage()]);
}