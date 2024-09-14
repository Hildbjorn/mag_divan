from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Файл со ссылками для парсинга
input_file = 'parser/unique_links.txt'
# Файл для сохранения уникальных ссылок
output_file = 'parser/extracted_links.txt'

# Множество для хранения уникальных ссылок
unique_links = set()

# Чтение ссылок из файла
with open(input_file, 'r', encoding='utf-8') as file:
    links = file.read().splitlines()

for link in links:
    # Инициализация драйвера для каждой ссылки
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(link)

        # Явное ожидание для загрузки элементов с классом tn-elem
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.tn-atom__sbs-anim-wrapper a.tn-atom')))

        # Находим все ссылки на модели
        model_links = driver.find_elements(
            By.CSS_SELECTOR, 'div.tn-atom__sbs-anim-wrapper a.tn-atom')

        for model_link in model_links:
            href = model_link.get_attribute('href')
            if href:  # Проверяем, что ссылка не пустая
                unique_links.add(href)  # Добавляем ссылку в множество

    except TimeoutException:
        print("Время ожидания истекло. Проверьте наличие элементов на странице.")
    except Exception as e:
        print(f'Ошибка: {e}')
    finally:
        driver.quit()  # Закрытие драйвера после обработки страницы

# Преобразуем множество в список
unique_links_list = list(unique_links)

# Сохранение уникальных ссылок в файл
with open(output_file, 'w', encoding='utf-8') as file:
    for url in unique_links_list:
        file.write(url + '\n')

print('------------------------------------')
print('Уникальные ссылки сохранены в файл extracted_links.txt')
print('------------------------------------')
