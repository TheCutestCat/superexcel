from pathlib import Path
import streamlit as st
from streamlit.web.bootstrap import run

def streamlit_app():
    # 这里导入并运行您的主 Streamlit 应用
    import superexcel.main

async def asgi_app(scope, receive, send):
    if scope["type"] == "http":
        run(streamlit_app, "", [], flag_options={})
        return
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    })
    await send({
        "type": "http.response.body",
        "body": b"Hello, World!",
    })

# 这个变量名很重要，Vercel 会查找它
app = asgi_app