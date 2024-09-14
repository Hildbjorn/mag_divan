from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Список ссылок
links = [
    "https://imperiya-idey.ru/catalog#!/tab/447644196-1",
    "https://imperiya-idey.ru/catalog#!/tab/447644196-2",
    "https://imperiya-idey.ru/catalog#!/tab/447644196-3",
    "https://imperiya-idey.ru/catalog#!/tab/447644196-4",
    "https://imperiya-idey.ru/catalog#!/tab/447644196-5",
    "https://imperiya-idey.ru/catalog#!/tab/447644196-6",
]

# Множество для хранения уникальных ссылок
unique_links = set()

for link in links:
    # Инициализация драйвера для каждой ссылки
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(link)

        # Явное ожидание для загрузки элементов с классом tn-elem
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[href^="catalog/"]')))

        # Находим все ссылки на модели диванов
        model_links = driver.find_elements(
            By.CSS_SELECTOR, 'a[href^="catalog/"]')

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
with open('parser/unique_links.txt', 'w', encoding='utf-8') as file:
    for url in unique_links_list:
        file.write(url + '\n')

print('------------------------------------')
print('Уникальные ссылки сохранены в файл unique_links.txt')
print('------------------------------------')
