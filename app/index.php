<?php

require_once './vendor/autoload.php';
require_once './src/bootstrap.php';

use App\Logger;
use App\ReviewSyncService;

$logger = new Logger();
$review = new ReviewSyncService();

// ログの例
$logger->info('アプリケーションが開始されました', [
    'user_id' => 123,
    'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
]);

// リクエストの処理
$action = $_GET['action'] ?? 'home';

switch ($action) {
    case 'home':
        $logger->info('ホームページにアクセスしました');
        echo "<h1>ホームページ</h1>";
        echo "<p>簡単なPHPアプリケーションです</p>";
        echo "<a href='?action=about'>About</a> | ";
        echo "<a href='?action=error'>エラーテスト</a> | ";
        echo "<a href='?action=reviews'>ElasticSearchへの登録</a>";
        break;

    case 'about':
        $logger->info('Aboutページにアクセスしました');
        echo "<h1>About</h1>";
        echo "<p>このアプリはElasticsearchにログを送信します</p>";
        echo "<a href='?action=home'>ホーム</a>";
        break;

    case 'error':
        $logger->error('テストエラーが発生しました', [
            'error_type' => 'test_error',
            'severity' => 'medium'
        ]);
        echo "<h1>エラーテスト</h1>";
        echo "<p>エラーログをElasticsearchに送信しました</p>";
        echo "<a href='?action=home'>ホーム</a>";
        break;

    case 'reviews':
        $review->syncReview();
        $logger->info('ElasticSearchに登録しました。');
        echo "<h1>レビューデータ登録</h1>";
        echo "<p>DBにあるレビューデータをElasticSearchに20件登録しました。</p>";
        echo "<a href='?action=home'>ホーム</a>";
        break;

    default:
        $logger->warning('不明なアクションへのアクセス', [
            'action' => $action,
            'url' => $_SERVER['REQUEST_URI'] ?? 'unknown'
        ]);
        echo "<h1>404 - ページが見つかりません</h1>";
        echo "<a href='?action=home'>ホーム</a>";
        break;
}

// ページの終了ログ
$logger->info('リクエストが完了しました', [
    'action' => $action,
    'response_time' => microtime(true) - $_SERVER['REQUEST_TIME_FLOAT']
]);


$response = $review->searchIndex('球');
if ($response['hits']['total']['value'] > 0) {
    $review = $response['hits']['hits'][0]['_source'];
    echo "タイトル: " . $review['title'] . "\n";
} else {
    echo "該当するレビューが見つかりません\n";
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PHP ELK Stack Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        a { color: #0066cc; text-decoration: none; margin: 0 10px; }
        a:hover { text-decoration: underline; }
        .info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="info">
        <h3>Kibanaでログを確認</h3>
        <p>Kibanaにアクセス: <a href="http://localhost:5601" target="_blank">http://localhost:5601</a></p>
        <p>インデックス名: <strong>php-app-logs</strong></p>
        <p>Elasticsearchに直接アクセス: <a href="http://localhost:9200" target="_blank">http://localhost:9200</a></p>
    </div>
</body>
</html>