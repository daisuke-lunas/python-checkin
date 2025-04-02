from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysettings
from mysql import connector
from mysql.connector import Error

load_dotenv()

app = Flask(__name__)
CORS(app)

"""やりたいこと
入店を記録する（MACアドレスで認証、チェックイン済みなら無視）
    チェック：今日入店しているか？
    入店していないなら、入店処理 -> いらっしゃいませ
    入店しているなら、貸出確認画面：品目、開始と終了を問う
備品の貸出や防音室の利用を記録する（MACアドレスで認証、入店記録がなければ無視）
    開始を記録する・終了を記録する：それぞれを受けるAPI
        DBとしてはcheckinに入れる
ユーザーを入力（ユーザー端末）
    チェック：そのMACアドレスが存在するか確認
    あるなら、無視
    ないなら、パスワード入力画面
ユーザーを登録処理
    チェック：そのMACアドレスが存在するか確認
    あるなら、無視
    ないなら、customerに登録

ゲストユーザーを（NFCタグによる）チェックイン等（全部操作できるようにする）
    お古のAndroid端末のみで受け付ければいいか

admin frontUI:
    今日入店しているcustomerの一覧を選べる
    今日のcheckinをとりあえず全部出す
    退店を記録する
        customerを選んだら、checkin一覧をリスト
        その人を退店させる：max時刻と、min時刻の、差分を表示


"""

"""
DB設計
checkin:
    id, customer_id, customer_name, datetime(now), type("in", "item", "room", "out" etc...), item, details
customer:
    id, name, type(joren, staff, admin), mac_address, bikou

"""


@app.route('/checkin', methods=['POST'])
def checkin():
    mac_address = request.json.get("mac_address", "MACアドレス不明")
    return jsonify({"message": f"受信したMACアドレス: {mac_address}"}), 200


def fetch_users():
    try:
        # MySQLサーバーへの接続
        connection = connector.connect(
            host='localhost',          # ホスト名
            user=mysettings.DB_USER_NAME,      # ユーザー名
            password=mysettings.DB_PASSWORD,  # パスワード
            database=mysettings.DB_NAME   # データベース名
        )

        if connection.is_connected():
            print("Connected to MySQL database")

            # クエリの実行
            query = "SELECT * FROM users"
            cursor = connection.cursor()
            cursor.execute(query)

            # 結果を取得
            results = cursor.fetchall()

            # 結果を表示
            for row in results:
                print(row)

    except Error as e:
        print(f"Error: {e}")

    finally:
        # リソースの解放
        if 'cursor' in locals() and cursor.is_connected():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    print("===   launch server   ===")
    app.run(host="0.0.0.0", port=8080)
    print("===   end server   ===")
