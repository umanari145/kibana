from elasticsearch import Elasticsearch


ELASTIC_SEARCH_PATH = "http://elasticsearch:9200"

class Els:
    
    def __init__(self):
        self.client = Elasticsearch(
            ELASTIC_SEARCH_PATH 
        )

    def main(self):
        print(self.client.info())

    # インデックスの作成
    def create_index(self):

        mapping = {
           "first_name": {
                "type": "text"
            },
            "last_name": {
                "type": "text"
            },
            "date_of_birth": {
               "type": "date",
               "format": "yyyy-MM-dd"
            },
            "position": {
                "type": "keyword"
            },
            "team": {
                "type": "keyword"
            },
            "avg": {
                "type": "float"
            },
            "hr": {
                "type": "integer"
            },
            "rbi": {
                "type": "integer"
            }}

        self.client.indices.create(
            index = "baseball_player_idx",
            body = {
                'mappings': {
                    'properties': mapping
                }
            })
    # documentの挿入
    def insert_document(self):
        list_of_players = [
          {
            "first_name": "清原",
            "last_name": "和博",
            "date_of_birth": "1967-08-18",
            "position": "一塁手",
            "team": "西武",
            "avg": 0.272,
            "hr": 525,
            "rbi": 1530
          },
          {
            "first_name": "落合",
            "last_name": "博満",
            "date_of_birth": "1953-12-09",
            "position": "一塁手",
            "team": "ロッテ",
            "avg": 0.311,
            "hr": 510,
            "rbi": 1564
          },
          {
            "first_name": "王",
            "last_name": "貞治",
            "date_of_birth": "1940-05-20",
            "position": "一塁手",
            "team": "巨人",
            "avg": 0.325,
            "hr": 868,
            "rbi": 2170
          },
          {
            "first_name": "長嶋",
            "last_name": "茂雄",
            "date_of_birth": "1936-02-20",
            "position": "三塁手",
            "team": "巨人",
            "avg": 0.305,
            "hr": 444,
            "rbi": 1522
          },
          {
            "first_name": "イチロー",
            "last_name": "鈴木",
            "date_of_birth": "1973-10-22",
            "position": "外野手",
            "team": "オリックス",
            "avg": 0.353,
            "hr": 21,
            "rbi": 68
          },
          {
            "first_name": "松井",
            "last_name": "秀喜",
            "date_of_birth": "1974-06-19",
            "position": "外野手",
            "team": "巨人",
            "avg": 0.304,
            "hr": 332,
            "rbi": 889
          },
          {
            "first_name": "野村",
            "last_name": "克也",
            "date_of_birth": "1935-06-29",
            "position": "捕手",
            "team": "南海",
            "avg": 0.277,
            "hr": 657,
            "rbi": 1982
          },
          {
            "first_name": "山本",
            "last_name": "浩二",
            "date_of_birth": "1946-10-25",
            "position": "外野手",
            "team": "広島",
            "avg": 0.290,
            "hr": 536,
            "rbi": 1475
          },
          {
            "first_name": "張本",
            "last_name": "勲",
            "date_of_birth": "1940-06-19",
            "position": "外野手",
            "team": "東映",
            "avg": 0.319,
            "hr": 504,
            "rbi": 1676
          },
          {
            "first_name": "立浪",
            "last_name": "和義",
            "date_of_birth": "1969-08-19",
            "position": "遊撃手",
            "team": "中日",
            "avg": 0.285,
            "hr": 171,
            "rbi": 1037
          }
        ]
        for id_doc, document in enumerate(list_of_players):
            self.client.index(
                index="baseball_player_idx",
                body=document,
                id=id_doc
            )

    # document更新
    def update_document(self, id):
        update_players = {
            "first_name": "翔平",
            "last_name": "大谷",
            "date_of_birth": "1994-07-05",
            "position": "指名打者/外野手",
            "team": "エンゼルス",
            "avg": 0.304,
            "hr": 44,
            "rbi": 95
        }
        self.client.index(
            index="baseball_player_idx",
            id=id,
            body={"doc": update_players}
        )

    # document削除
    def delete_document(self, id):
        self.client.delete(
            index="baseball_player_idx",
            id=id
        )

    def match_query(self):
        query = {
            "query": {
                "match": {
                    "first_name": "清原"
                }
            }
        }
        return self.client.search(
            index="baseball_player_idx",
            body=query
        )

    def match_multi_query(self):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "date_of_birth": {
                                "gte": "1960-01-01",
                                "format": "yyyy-MM-dd"
                                }
                            }
                       },
                        {
                            "range": {
                                "hr": {
                                "gte": 500
                                }
                            }
                        }
                    ]
                }
            }
        }

        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "term": {
                            "position": "外野手"
                            }
                        },
                        {
                            "term": {
                                "team": "西武"
                            }
                        }
                    ],
                "minimum_should_match": 1
                }
            }
        }

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "first_name": "イチロー"
                            }
                        },
                        {
                            "match": {
                                "team": "オリックス"
                            }
                        }
                    ]
                }
            }
        }

        return self.client.search(
            index="baseball_player_idx",
            body=query
        )


es = Els()
#es.create_index()
#es.insert_document()
#es.update_document(9)
#res = es.delete_document(9)
#print(es.match_query())
print(es.match_multi_query())