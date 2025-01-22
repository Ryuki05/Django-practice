pip install django-tailwind
pip install mysqlclient
pip install path\to\mysqlclient‑X.X.X‑cpXXX‑win_amd64.whl
python manage.py migrate

Djangoプロジェクトのディレクトリで以下のコマンドを実行します：


python manage.py createsuperuser
2. プロンプトに従って情報を入力
コマンドを実行すると、以下のようなプロンプトが表示されます。指示に従って入力してください：


Username (leave blank to use 'your-username'): admin  # 好きなユーザー名を入力
Email address: admin@example.com                      # メールアドレスを入力
Password:                                             # パスワードを入力（非表示）
Password (again):                                     # 確認のため再入力
注意: パスワードは非表示ですが、設定が強いパスワードでないとエラーが出る場合があります。簡単なパスワードを使用する場合は、開発環境で以下のように入力してスキップできます：
text
コピーする
編集する
Bypass password validation and create user anyway? [y/N]: y
3. スーパーユーザーの作成が成功
すべて正常に入力すると、以下のようなメッセージが表示されます：

text
コピーする
編集する
Superuser created successfully.


メニューバーから「View」→「Command Palette(Ctrl+Shift+P)」を選ぶ。
cursor_japanese_01.png

立ち上がったコマンドパレットから「Configure Display Language」を選択する。
cursor_japanese_02.png

「日本語(ja)」を選択する。
cursor_japanese_03.png

「日本語に切り替えるためにCursorを再起動するか？」みたいなウインドウが出てくるので、「Restart」をクリックする。