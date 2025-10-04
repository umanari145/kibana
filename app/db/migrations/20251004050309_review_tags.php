<?php

declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class ReviewTags extends AbstractMigration
{
    /**
     * Change Method.
     *
     * Write your reversible migrations using this method.
     *
     * More information on writing migrations is available here:
     * https://book.cakephp.org/phinx/0/en/migrations.html#the-change-method
     *
     * Remember to call "create()" or "update()" and NOT "save()" when working
     * with the Table class.
     */
    public function up()
    {
        $table = $this->table('review_tags', ['id' => false, 'primary_key' => ['review_id', 'tag_id']]);
        $table->addColumn('review_id', 'integer', [
                'signed' => false,
                'null' => false
            ])
            ->addForeignKey('review_id', 'reviews', 'id', [
                'delete' => 'CASCADE',
                'update' => 'NO_ACTION'
            ])
            ->addColumn('tag_id', 'integer', [
                'signed' => false,
                'null' => false
            ])
            ->addForeignKey('tag_id', 'tags', 'id', [
                'delete' => 'CASCADE',
                'update' => 'NO_ACTION'
            ])
            ->addColumn('created_at', 'timestamp', [
                'null' => true,
                'default' => null
            ])
            ->create();
    }

    public function down()
    {
        $this->table('review_tags')->drop()->save();
    }
}

