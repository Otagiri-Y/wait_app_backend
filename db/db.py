import os
import tempfile
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy インスタンスの作成
db = SQLAlchemy()

# SSL証明書を含むデータベース設定を行う関数
def configure_database(app):
    """
    Flaskアプリケーションにデータベース設定を追加する関数。
    環境変数からデータベース接続情報とSSL証明書を取得。
    """
    # データベースURLを環境変数から作成
    DATABASE_URL = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    
    # SSL証明書の内容を環境変数から取得
    pem_content = os.getenv("DB_SSL_CA")
    if pem_content:
        # 改行コード（\n）を元の改行に戻す
        pem_content = pem_content.replace("\\n", "\n").replace("\\", "")

        # 一時ファイルを作成し、SSL証明書を保存
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".pem") as temp_pem:
            temp_pem.write(pem_content)
            temp_pem_path = temp_pem.name

        # データベースURLにSSL設定を追加
        DATABASE_URL += f"?ssl_ca={temp_pem_path}"
    else:
        raise ValueError("SSL証明書の環境変数 DB_SSL_CA が設定されていません。")

    # FlaskアプリケーションにデータベースURIを設定
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SQLAlchemyをアプリに初期化
    db.init_app(app)