import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
import mysql.connector
from mysql.connector import Error
import settings

load_dotenv()

app = Flask(__name__)
CORS(app)

"""やりたいこと
1: パラメータからユーザーを取得してチェックイン記録をDBに登録する（端末のMACアドレスで認識する）
2-2: frontUIからアクセスされてデータを返すAPI

"""


def get_mac_address(ip_address):
    """
    指定されたIPアドレスに対応するMACアドレスを取得
    """
    try:
        # ARPテーブルを確認する
        output = subprocess.check_output(
            f"arp -n {ip_address}", shell=True).decode()
        # MACアドレスのパターンを探す
        for line in output.splitlines():
            if ip_address in line:
                mac = line.split()[2]
                return mac
    except Exception as e:
        print(f"エラー: {e}")
    return None


@app.route('/')
def index():
    # クライアントのIPアドレスを取得
    client_ip = request.remote_addr
    # MACアドレスを取得
    mac_address = get_mac_address(client_ip)

    if mac_address:
        return f"クライアントのMACアドレス: {mac_address}"
    else:
        return "MACアドレスを取得できませんでした"


def fetch_users():
    try:
        # MySQLサーバーへの接続
        connection = mysql.connector.connect(
            host='localhost',          # ホスト名
            user=settings.DB_USER_NAME,      # ユーザー名
            password=settings.DB_PASSWORD,  # パスワード
            database=settings.DB_NAME   # データベース名
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
