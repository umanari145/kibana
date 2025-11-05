import csv
import json
import requests
import sys

# --- 設定 ---
ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "products_index"
CSV_FILE = "products.csv"
BULK_API_ENDPOINT = f"{ES_HOST}/_bulk"

def prepare_bulk_data(csv_file, index_name):
    """
    CSVファイルを読み込み、ElasticsearchのバルクAPI形式のイテレータを生成する。
    """
    print(f"CSVファイル '{csv_file}' を読み込み中...")
    
    # データを保存するためのリスト
    bulk_actions = []

    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # 1. メタデータ行の作成
                # product_idをドキュメントのIDとして使用
                metadata = {
                    "create": {
                        "_index": index_name,
                        "_id": row['product_id']
                    }
                }
                
                # 2. ドキュメント本体の作成（型の調整）
                doc = {}
                for key, value in row.items():
                    # 値が空文字でないことを確認
                    if not value:
                        doc[key] = None
                        continue

                    # 型の変換
                    if key in ['price']:
                        doc[key] = float(value)
                    elif key in ['stock_count']:
                        # 整数に変換。変換できない場合はそのまま保持
                        try:
                            doc[key] = int(float(value)) 
                        except ValueError:
                            doc[key] = value
                    elif key in ['is_available']:
                        # 'TRUE' / 'FALSE' を Python の True / False に変換
                        doc[key] = value.upper() == 'TRUE'
                    else:
                        # その他の文字列や日付はそのまま
                        doc[key] = value
                
                # バルクアクションリストに追加（メタデータとドキュメント本体を順番に追加）
                bulk_actions.append(json.dumps(metadata))
                bulk_actions.append(json.dumps(doc))

    except FileNotFoundError:
        print(f"エラー: ファイル '{csv_file}' が見つかりません。")
        sys.exit(1)
    except Exception as e:
        print(f"CSV処理中にエラーが発生しました: {e}")
        sys.exit(1)

    # アクションを改行で結合し、末尾に改行を追加してバルクAPI形式にする
    return "\n".join(bulk_actions) + "\n"

def send_bulk_data(bulk_data):
    """
    Elasticsearchの_bulk APIにデータを送信する。
    """
    print(f"Elasticsearch ({BULK_API_ENDPOINT}) にデータを投入中...")
    
    headers = {'Content-Type': 'application/x-ndjson'} # バルクAPIはNDJSON形式
    
    try:
        response = requests.post(
            BULK_API_ENDPOINT, 
            headers=headers, 
            data=bulk_data, 
            timeout=30 # タイムアウト設定
        )
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        
        result = response.json()
        
        if result.get("errors"):
            print("\n!!! バルク投入中にエラーが発生しました。詳細を確認してください。!!!")
            # 最初の5つのエラー詳細を表示
            error_count = sum(item.get("error") is not None for item in result["items"])
            print(f"合計 {error_count} 件の投入エラーがありました。")
            return
        
        print("\n=== データ投入成功 ===")
        print(f"投入されたドキュメント数: {len(result['items'])}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n!!! Elasticsearch接続エラー !!!")
        print(f"ホスト {ES_HOST} に接続できません。Elasticsearchが起動しているか確認してください。")
        print(f"詳細: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"不明なエラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 1. インデックスの存在確認・作成（オプション：手動で作成済みを想定）
    # 2. バルクデータの準備
    bulk_data = prepare_bulk_data(CSV_FILE, INDEX_NAME)
    print(bulk_data)
    # 3. データの送信
    send_bulk_data(bulk_data)