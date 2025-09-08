#!/bin/bash

# このファイル自体は、開発環境で使えるようにするため、chmod +x entrypoint.sh をする必要がある。
# これは volume によってコンテナ内のファイルを上書き（マスク）するため。
# また本番環境では、イメージの中に焼き付けられた entrypoint.sh が使われる(volumeは使わない)
# ので、Dockerfileの中の RUN chmod +x entrypoint.sh は必要。

# スクリプト内で実行したコマンドが一つでも失敗（エラーで終了）した場合、その場でスクリプト全体を即座に終了させる
set -e

# FLASK_DEBUGが'1'に設定されているかどうかでコマンドを切り替える
if [ "${APP_ENV}" = "development" ]; then
    # 開発モード
    echo "Starting development server with Flask (FLASK_DEBUG=1)..."
    # 開発時は、コンテナ内では常に5000番でリッスンする。デフォルト値なので --port=5000 は書かなくてもいい。
    exec flask run --host=0.0.0.0 --port=5000
else
    # 本番モード
    echo "Starting production server with Gunicorn..."
    # 環境変数 PORT があればそれを使い、なければデフォルトで 5000 を使う
    exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers ${GUNICORN_WORKERS:-4} --timeout ${GUNICORN_TIMEOUT:-120} "app:create_app()"
fi
