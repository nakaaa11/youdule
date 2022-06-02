def search_channel_ids(name):
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver_path = "/Users/nak/Desktop/python_lesson/scraping/chromedriver"
    brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.binary_location = brave_path
    brave = webdriver.Chrome(executable_path=driver_path, options=option)

    c = []

    brave.get(f'https://www.youtube.com/results?search_query={name}')
    brave.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer/div/div[1]/a/div/yt-img-shadow/img').click()
    brave.refresh()
    channel = brave.find_element(By.XPATH, '/html/body/link')
    c.append(channel.get_attribute("href"))
    return str(c[0]).replace("https://www.youtube.com/channel/", "")
