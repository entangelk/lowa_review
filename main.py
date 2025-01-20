def get_data (url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from pymongo import MongoClient
    from datetime import datetime
    import re
    import time

    def safe_click(driver, element):
        try:
            # 스크롤을 요소가 있는 곳까지 내림
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            
            # 방해 요소들 제거
            driver.execute_script("""
                var overlays = document.querySelectorAll('._15wa8-0F_5');
                overlays.forEach(function(overlay) {
                    overlay.remove();
                });
            """)
            
            # JavaScript로 클릭 실행
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            # 직접 URL로 이동
            href = element.get_attribute('href')
            if href:
                driver.get(f"https://smartstore.naver.com{href}")
            else:
                raise e
            
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['lowa_db']

    # 웹드라이버 설정
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # URL 설정 및 페이지 로딩
    # url = "https://smartstore.naver.com/lowakorea"
    driver.get(url)

    time.sleep(2)


    more_button = driver.find_element(By.CSS_SELECTOR, "#pc-categoryMenuWidget > div > div > div > div > div > div._1AJ8D2PjS4._3nO3wKj4-Z > button")
    more_button.click()  
    time.sleep(2)

    review_button = driver.find_element(By.CSS_SELECTOR, "#pc-categoryMenuWidget > div > div > div > div > div > div._1AJ8D2PjS4 > div > ul._3AV7RVieRB > li._2jm5JW3D5W.type_white_gnb.YI_nVHGI_0.N\=a\:lca\.all > a")
    review_button.click()    

    time.sleep(2)

    item_elements = driver.find_elements(By.CSS_SELECTOR, "#CategoryProducts > ul > li")

    for idx, elment in enumerate(item_elements,1):
        # review_button = driver.find_element(By.CSS_SELECTOR, "#pc-wholeProductWidget > div > div > div > div > div._3qyVpgraNa > div > ul > li:nth-child(7) > button")
        # review_button.click()



        time.sleep(2)

        try:
            more_button = driver.find_element(By.CSS_SELECTOR, "#pc-categoryMenuWidget > div > div > div > div > div > div._1AJ8D2PjS4._3nO3wKj4-Z > button")
            more_button.click()  
            time.sleep(2)

            review_button = driver.find_element(By.CSS_SELECTOR, "#pc-categoryMenuWidget > div > div > div > div > div > div._1AJ8D2PjS4 > div > ul._3AV7RVieRB > li._2jm5JW3D5W.type_white_gnb.YI_nVHGI_0.N\=a\:lca\.all > a")
            review_button.click()    

            time.sleep(2)
        except:
            pass

        refind_elment = driver.find_element(By.CSS_SELECTOR, "#CategoryProducts > ul")
        product = refind_elment.find_element(By.CSS_SELECTOR,f"li:nth-child({idx}) > div > a")
        # product = elment.find_element(By.CSS_SELECTOR,f"li > div > a")
        
        
        
        
        try:
            # safe_click 함수 사용
            safe_click(driver, product)
        except:
                        # 방해되는 요소 제거
            driver.execute_script("""
                var element = document.querySelector('._15wa8-0F_5');
                if(element)
                    element.remove();
            """)
            product.click()

        time.sleep(2)
        product_name = driver.find_element(By.CSS_SELECTOR, "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3").text
        price_raw =  driver.find_element(By.CSS_SELECTOR, "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR").text
        price = int(re.sub(r'[^0-9]', '', price_raw))
        time.sleep(2)
        
        review_button = driver.find_element(By.CSS_SELECTOR, "#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a")
        
        review_button.click()  


        time.sleep(2)



        while True:

            review_button = driver.find_element(By.CSS_SELECTOR, "#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a")
            
            review_button.click()  
            

            review_elements = driver.find_elements(By.CSS_SELECTOR, "#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li")
            
            for review in review_elements:
              
                try:
                    writer = review.find_element(By.CSS_SELECTOR, "div > div > div > div._3-1uaKhzq4 > div > div._1McWUwk15j > div._3i1mVq_JBd > div._3HKlxxt8Ii > div.iWGqB6S4Lq > strong").text
                except:
                    writer = ''

                try:
                    date = review.find_element(By.CSS_SELECTOR, "div > div > div > div._3-1uaKhzq4 > div > div._1McWUwk15j > div._3i1mVq_JBd > div._3HKlxxt8Ii > div.iWGqB6S4Lq > span").text
                except:
                    date = ''


                try:
                    size = review.find_element(By.CSS_SELECTOR, "div > div > div > div._3-1uaKhzq4 > div > div._1McWUwk15j > div._3i1mVq_JBd > div._3HKlxxt8Ii > div._2FXNMst_ak").text
                except:
                    size = ''

                try:
                    content = review.find_element(By.CSS_SELECTOR, "div > div > div > div._3-1uaKhzq4 > div > div._1McWUwk15j > div._3z6gI4oI6l").text
                    
                except:
                    content = ''

                try:
                    rate = review.find_element(By.CSS_SELECTOR, "div > div > div > div._3-1uaKhzq4 > div > div._1McWUwk15j > div._3i1mVq_JBd > div._3HKlxxt8Ii > div._2V6vMO_iLm > em").text
                    
                    rate = int(rate)
                except:
                    rate = ''

                # MongoDB에 바로 저장
                review_data = {
                    'product_name': product_name,
                    'product_price': price,
                    'writer' : writer,
                    'content': content,
                    'size': size,
                    'date': date,
                    'rate': rate
                }
                
                db.reviews.insert_one(review_data)


            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a.fAUKm1ewwo._2Ar8-aEUTq._nlog_click")
                next_button.click() 
                time.sleep(2)
            except:
                break

        driver.back()



    # 브라우저 종료
    driver.quit()


if __name__ == "__main__":
    url = "https://smartstore.naver.com/lowakorea"
    get_data (url)
    pass