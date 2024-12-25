import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager




def solve_captcha(browser):
    while "https://elibrary.ru/page_captcha" in browser.current_url:
        print("Решите капчу")
        WebDriverWait(browser, 30).until(lambda d: d.current_url != "https://elibrary.ru/page_captcha")
        time.sleep(5)




def next_page(browser):
    browser.find_element(By.XPATH,"/html/body/div[3]/table/tbody/tr/td/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[2]/div[2]/div/table/tbody/tr[2]/td[2]/a").click()




def get_publication_info(browser, pub_id, pub_counter, author_id):
    browser.get(f'https://www.elibrary.ru/item.asp?id={pub_id}')
    solve_captcha(browser)
    try:
        pub_name = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bigtext"))
        )
        pub_name_text = pub_name.text.strip()
        print(f"{pub_counter}. Название публикации: {pub_name_text}")
        print(f"   Ссылка на публикацию: https://www.elibrary.ru/item.asp?id={pub_id}")
    except Exception as e:
        print(f"Ошибка при получении информации о публикации ID {pub_id}: {e}")
    finally:
        browser.get(f'https://www.elibrary.ru/author_items.asp?authorid={author_id}&show_refs=1&show_option=1')
        solve_captcha(browser)




def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)



    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    stealth(browser,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True)



    author_id = input("Введите ID автора: ").strip()
    


    if author_id.isdigit() and len(author_id) <= 7:
        solve_captcha(browser)
        browser.get(f'https://www.elibrary.ru/author_items.asp?authorid={author_id}&show_refs=1&show_option=1')
        solve_captcha(browser)
        publication_counter = 1
        


        while True:
            try:
                publications_block = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "select-tr-left"))
                )


                if publication_counter % 20 == 1 and publication_counter != 1: 
                    next_page(browser)
                


                if publication_counter > len(publications_block):
                    print("Все публикации обработаны.")
                    break
                


                publication = publications_block[publication_counter - 1]
                name_element = publication.find_element(By.TAG_NAME, 'a')
                publication_id = name_element.get_attribute('name')[1:] 
                get_publication_info(browser, publication_id, publication_counter, author_id)
                publication_counter += 1
            except Exception as e:
                print(f"Ошибка при обработке публикации {publication_counter}: {e}")
                break 
                


    else:
        print("Введенный ID недействителен")



    browser.quit()




if __name__ == "__main__":
    main()