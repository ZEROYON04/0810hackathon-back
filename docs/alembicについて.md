# alembic

pythonのsqlalchemyで作成したモデルと実際のデータベースのスキーマを同期させるツールです。
1. alembic.iniの`sqlalchemy.url = `の部分にデータベースのURLを設定
2. `alembic/env.py`の`target_metadata`にsqlalchemyのベースモデルのメタデータを代入
3. `alembic revision --autogenerate -m "任意のメッセージ"`でデータベースをモデル定義に同期させるためのマイグレーションファイルを作成できます。
4. 別のデータベースの接続設定を行ったあとに`alembic upgrade head`を実行することによってデータベースのスキーマを同期することができます。

## 注意点
同期させる順番が重要になるので、どんなデータベースでも任意の状態にすぐ同期できるわけではないようです。