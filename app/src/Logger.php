<?php

namespace App;

use Elastic\Elasticsearch\ClientBuilder;
use Monolog\Logger as MonologLogger;
use Monolog\Handler\ElasticsearchHandler;
use Monolog\Formatter\ElasticsearchFormatter;

class Logger
{
    private $logger;

    public function __construct()
    {
        $client = ClientBuilder::create()
            ->setHosts(['http://elasticsearch:9200'])
            ->build();
        // Monologロガーを作成
        $this->logger = new MonologLogger('php-app');

        // Elasticsearchハンドラーを作成
        $handler = new ElasticsearchHandler($client, [
            'index' => 'php-app-logs',
            'type' => '_doc'
        ]);

        // フォーマッターを設定
        $handler->setFormatter(new ElasticsearchFormatter('php-app-logs', '_doc'));

        // ハンドラーをロガーに追加
        $this->logger->pushHandler($handler);
    }

    public function info($message, array $context = [])
    {
        $this->logger->info($message, $context);
    }

    public function warning($message, array $context = [])
    {
        $this->logger->warning($message, $context);
    }

    public function error($message, array $context = [])
    {
        $this->logger->error($message, $context);
    }

    public function debug($message, array $context = [])
    {
        $this->logger->debug($message, $context);
    }
}