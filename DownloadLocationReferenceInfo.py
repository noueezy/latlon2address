import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

# ダウンロード終了まで待機（＝指定したパスのファイルの存在が確認できるまで待機）
def wait_for_dl_complete(dl_file):
    while os.path.exists(dl_file) == False:
        time.sleep(0.1)
        

def download_location_reference_info(dl_path, chromedriver_path):

    # ファイル保存先ディレクトリ作成
    os.makedirs(dl_path)

    # chromオプションにてファイル保存先を指定
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : dl_path}
    chromeOptions.add_experimental_option("prefs",prefs)

    # chrome起動
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chromeOptions)

    # 操作するページを開く
    driver.get('http://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi')


    # ページ GUI自動操作

    # 1ページ目
    driver.find_element_by_xpath("//input[@type='submit' and @value='　都道府県単位　']").click()

    # 2ページ目
    driver.find_element_by_id('allac').click()
    driver.find_element_by_xpath("//input[@type='submit' and @value='　　選　択　　']").click()

    # 3ページ目
    driver.find_element_by_id('all_choaza2').click()
    driver.find_element_by_xpath("//input[@type='submit' and @value='　　選　択　　']").click()

    # 4ページ目
    driver.find_element_by_xpath("//input[@type='submit' and @value='　 同意する 　']").click()

    # 5ページ目（ダウンロードページ)
    td_element = driver.find_element_by_xpath("/html/body/div[4]/table/tbody/tr[2]/td[2]/div/form/div[2]/table/tbody/tr/td")
    tables = td_element.find_elements_by_tag_name("table")

    tableNum = len(tables)

    for i in range(tableNum):
        no = i + 1

        table_rows = tables[i].find_elements_by_tag_name("tr")
        
        #大字・町丁目レベル版数取得
        oaza_col = table_rows[2].find_elements_by_tag_name("td")
        oaza_ver = oaza_col[5].find_element_by_tag_name("font").text

        #ダウンロードファイル名
        oaza_dl_name = str(no).zfill(2)+'000-'+oaza_ver

        if dl_path[-1] != "/":
            dl_path = dl_path + "/"
    
        oaza_dl_path = dl_path + oaza_dl_name + '.zip'

        driver.find_element_by_name(oaza_dl_name).click()
        Alert(driver).accept()
        wait_for_dl_complete(oaza_dl_path)

    driver.quit()

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        sys.exit("Error")
    dl_path = os.getcwd() + '/data'
    chromedriver_path = args[1]
    download_location_reference_info(dl_path,chromedriver_path)