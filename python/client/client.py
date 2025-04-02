import streamlit as st
import requests
import uuid

# クエリパラメータを取得
print(st.query_params)
page = st.query_params.get("page", "")

# MACアドレス取得


def get_mac_address():
    mac_int = uuid.getnode()
    mac_hex = f"{mac_int:012x}"
    mac_address = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
    return mac_address


# UI
st.title("Streamlit Check-in System")

if page == "checkin":
    st.write("ボタンを押してチェックインしてください。")
    if st.button("チェックイン"):
        mac_address = get_mac_address()
        server_url = "http://localhost:8080/checkin"
        response = requests.post(server_url, json={"mac_address": mac_address})

        if response.status_code == 200:
            st.success(f"サーバーからの応答: {response.json()['message']}")
        else:
            st.error("エラーが発生しました。")
else:
    st.write("メインページです。")
