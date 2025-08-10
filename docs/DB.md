# データベースについて

## データベースの設定

compose.ymlの中にほぼすべての設定が記載されています。
また初期化は`db/init.sql`で行っていてスキーマはそこに記載されています。

## データベースへのターミナルからの接続

DBへの接続方法はdocker composeで起動した後`docker exec -it 0810hackathon-back-db-1 psql -U user -d mydatabase`を実行するとDBの操作が可能。

## sqlacodegenについて
sqlacodegenを使用するとDBの構造から自動的に対応するORMを生成できます。DBのスキーマを更新するときにはこれを実行してORMの更新を行って下さい。

## 拡張機能を使った接続

以下２つの拡張機能をインストールすると.vscodeディレクトリから設定を読み出して接続ができる。

- <https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-pg>
- <https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools>

## .pumlファイルについて

ER図を書くためのPlantUMLのファイルです。
実際に生成されたER図が.pngファイルとしてあるので自分で.pumlファイルを見れるようにしなくても大丈夫です。
