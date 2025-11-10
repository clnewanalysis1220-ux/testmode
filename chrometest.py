import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://clean-lease-gw.net/scripts/dneo/appsuite.exe?cmd=cdbasetappmanage&app_id=287#cmd=cdbasetrecalc"

USER_ID = os.getenv("GROUPWARE_USER")
PASSWORD = os.getenv("GROUPWARE_PASS")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        print("ページにアクセス中...")
        driver.get(URL)

        wait.until(EC.presence_of_element_located((By.NAME, "UserID")))
        print("ログインフォーム入力中...")
        driver.find_element(By.NAME, "UserID").send_keys(USER_ID)
        driver.find_element(By.NAME, "_word").send_keys(PASSWORD)
        driver.find_element(By.NAME, "_word").send_keys(Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cdb-recalculate-button")))
        print("ログイン完了")

        while True:
            print("チェックボックス確認中...")
            checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]')))
            if not checkbox.is_selected():
                checkbox.click()
                print("チェックボックスにチェックを入れました")
            else:
                print("チェックボックスはすでにチェック済み")

            print("再計算ボタンをクリック...")
            recalc_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cdb-recalculate-button")))
            recalc_button.click()

            print("再計算完了待機中...")
            time.sleep(10)  # 必要に応じ適宜調整

            print("1時間待機後再実行します")
            time.sleep(3600)

    except Exception:
        print("エラー発生:")
        traceback.print_exc()

    finally:
        driver.quit()
        print("ブラウザを終了しました")

if __name__ == "__main__":
    if not USER_ID or not PASSWORD:
        print("環境変数 GROUPWARE_USER および GROUPWARE_PASS をセットしてください")
    else:
        main()
