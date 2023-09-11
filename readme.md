# GF Scout System

<p>
  <a href="./LICENSE" target="_blank">
    <img alt="License: GNU General Public License 3.0" src="https://img.shields.io/badge/License-GNU General Public License 3.0-yellow.svg" />
  </a>
</p>

## 📌 Description

1. 紀錄童軍團內的團員、三項登記、階級(升團)、進程考驗、專科章考驗、活動、服務等資料
2. 管理員可以進行各項操作
   - 帳號的新增、編輯
   - 團員資料的新增、編輯
   - 三項登記的新增、刪除
   - 階級(升團)的新增、刪除
   - 進程考驗的新增、刪除
   - 專科章考驗的新增、刪除
   - 活動新增、編輯、刪除
   - 服務新增、編輯、刪除
   - 一般使用者(團員)的各項操作
3. 一般使用者(團員):有註冊帳號者
   - 登入、登出
   - 編輯自己的團員資料
   - 查詢自己的各項資料:
     - 團員資料
     - 三項登記
     - 階級(升團)
     - 進程考驗
     - 專科章考驗
     - 活動(可看到自己在活動中是參加人員亦或工作人員)
     - 服務
   - 新增自己的各項資料:
     - 進程考驗
     - 專科章考驗
     - 活動
     - 服務

## 📌 Requirement

    Frontend: Flask, Bootstrap, jQuery
    Backend: Flask, SQLAlchemy, SQLite

## 📌 Build Setup

### Use virtual environment

   1. Create a new environment
        ```shell
        python3 -m venv venv
        ```

   2. Activate the environment
      - mac os
        ```shell
        source venv/bin/activate
        ```

      - windows
        ```shell
        # 先進到放bat檔的資料夾裡
        cd ./venv/Scripts
        # 執行bat檔
        activate.bat
        # 看到命令行前面出現`(venv)`的時候就可以回到專案資料夾
        cd ../../
        ```

### Install python package

    ```shell
    pip3 install -r requirements.txt
    ```

### Create database file

    ```shell
    python3 ./create_db.py
    ```

### Run flask app

    ```shell
    flask --app website run 
    ```

    if you want to run in development mode, add `--debug` after `run`

    ```shell
    flask --app website run --debug
    ```

## 📌 Support & Author

👤 **Andy Lee** (u096169@gmail.conm)<br />

## 📌 License

This project is [GNU General Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.html) licensed.

## 📌 Version Informatio

 - v1.1.1 (Update data:2023.09.05)
   - 完成整個網站系統的大致架構
   - 管理員身份可操作之相關已完成
   - 非管理員身份暫時僅可觀看與其本身相關之紀錄

 - v1.1.7 (Update data:2023.09.11)
   - 非管理員身分可新增部分紀錄
   - 管理員身份部分介面修正
