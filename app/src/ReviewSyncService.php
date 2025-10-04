<?php

namespace App;

use Elastic\Elasticsearch\ClientBuilder;
use Illuminate\Database\Capsule\Manager as DB;

class ReviewSyncService
{
    private $client;

    public function __construct()
    {
        $this->client = ClientBuilder::create()
            ->setHosts(['http://elasticsearch:9200'])
            ->build();
    }

    public function syncReview(): void
    {
        $reviews = DB::table('reviews')
            ->select('reviews.*')
            /*->selectSub(function ($query) {
                $query->from('review_tags')
                    ->join('tags', 'review_tags.tag_id', '=', 'tags.id')
                    ->whereColumn('review_tags.review_id', 'reviews.id')
                    ->select(DB::raw('JSON_ARRAYAGG(JSON_OBJECT("id", tags.id, "name", tags.tag_name))'));
            }, 'tags_json')*/
            ->get();

        foreach ($reviews as $review) {
            try {
                // オブジェクト型でないとESに入らないためここで
                $tags = DB::table('review_tags')
                    ->join('tags', 'review_tags.tag_id', '=', 'tags.id')
                    ->where('review_tags.review_id', $review->id)
                    ->select('tags.id', 'tags.tag_name')
                    ->get();

                // ElasticSearchに保存
                $this->client->index([
                    'index' => 'reviews',
                    'id' => $review->id,
                    'body' => [
                        'title' => $review->title ?? '',
                        'content' => $review->content ?? '',
                        'tags' => $tags->toArray(),
                        'created_at' => $review->created_at
                    ]
                ]);
            } catch (\Exception $e) {
                    echo "✗ レビューID {$review->id} の同期に失敗: {$e->getMessage()}\n";
            }
        }
    }

    public function searchIndex(string $keyword)
    {
        // キーワードで検索して最初の1件を取得
        $response = $this->client->search([
            'index' => 'reviews',
            'body' => [
                'query' => [
                    'match' => [
                        'content' => $keyword
                    ]
                ],
                'size' => 1  // 1件だけ取得
            ]
        ]);
        return $response;
    }
}