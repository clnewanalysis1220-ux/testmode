import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 環境変数からログイン情報取得（本番運用では必須）
URL = "https://clean-lease-gw.net/scripts/dneo/appsuite.exe?cmd=cdbasetappmanage&app_id=287#cmd=cdbasetrecalc"
USER_ID = os.getenv("GROUPWARE_USER")
PASSWORD = os.getenv("GROUPWARE_PASS")

def main():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)  # 最大20秒の明示的待機設定

    try:
        print("ページにアクセス中...")
        driver.get(URL)

        # ログインフォームの要素が現れるまで待機
        wait.until(EC.presence_of_element_located((By.NAME, "UserID")))

        print("ログインフォームに入力中...")
        driver.find_element(By.NAME, "UserID").send_keys(USER_ID)
        driver.find_element(By.NAME, "_word").send_keys(PASSWORD)
        driver.find_element(By.NAME, "_word").send_keys(Keys.ENTER)

        # ログイン後の遷移で再計算ボタンがあるページまで待機
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cdb-recalculate-button")))
        print("ログイン完了")

        while True:
            print("チェックボックスをチェック中...")
            checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]')))
            if not checkbox.is_selected():
                checkbox.click()
                print("チェックボックスにチェックを入れました")
            else:
                print("チェックボックスはすでにチェック済みです")

            print("再計算ボタンをクリックします...")
            recalc_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cdb-recalculate-button")))
            recalc_button.click()

            print("再計算ボタンをクリックしました。完了を待機しています...")
            # 適宜ここはAJAXやページの変化を確認できる仕組みが良いですが、一旦固定待機
            time.sleep(10)

            print("再計算処理完了か要確認してください。1時間後に再実行します。")
            time.sleep(3600)

    except Exception:
        print("エラーが発生しました:")
        traceback.print_exc()  # 詳細なスタックトレースを表示

    finally:
        driver.quit()
        print("ブラウザを閉じました。")

if __name__ == "__main__":
    if not USER_ID or not PASSWORD:
        print("環境変数 CLEAN_LEASE_USER_ID および CLEAN_LEASE_PASSWORD を設定してください。")
    else:
        main()
