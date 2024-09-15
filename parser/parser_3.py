from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json

# Чтение URL-адресов из файла
with open('parser/extracted_links.txt', 'r', encoding='utf-8') as file:
    model_urls = [line.strip() for line in file if line.strip()]

catalog = {}

for url in model_urls:
    # Инициализация драйвера внутри цикла
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    try:
        # Ждем, пока загрузится необходимый элемент (например, название модели)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.t-menu__link-item[href*="/catalog#!/tab"]')))

        # Получаем тип мебели из данных модели
        type_name = driver.find_element(
            By.CSS_SELECTOR, 'a.t-menu__link-item[href*="/catalog#!/tab"]').text

        # Извлечение данных с страницы
        model_data = {
            'name': driver.find_element(By.CSS_SELECTOR, 'div.t396__elem.tn-elem.tn-elem__4869838811650541045869.t-animate.t-animate_started .tn-atom').text,
            'title': driver.find_element(By.CSS_SELECTOR, 'div.t396__elem.tn-elem.tn-elem__4869838811650541045869.t-animate.t-animate_started .tn-atom').text,
            # 'description': driver.find_element(By.CSS_SELECTOR, 'div.model-description').text,
            # 'type': driver.find_element(By.CSS_SELECTOR, 'span.model-type').text,
            # 'images': [img.get_attribute('src') for img in driver.find_elements(By.CSS_SELECTOR, 'div.model-images img')],
            # 'sleeping_area': driver.find_element(By.CSS_SELECTOR, 'span.sleeping-area').text,
            # 'length': driver.find_element(By.CSS_SELECTOR, 'span.length').text,
            # 'depth': driver.find_element(By.CSS_SELECTOR, 'span.depth').text,
            # Добавьте другие поля по мере необходимости
        }

        print('\nmodel_data: ', type_name)
        print('\nmodel_data: ', model_data, '\n')

        # # Если тип еще не добавлен в каталог, создаем его
        # if type_name not in catalog:
        #     catalog[type_name] = {
        #         'type_name': type_name,
        #         'model': []
        #     }

        # model_entry = {
        #     'model_name': model_data.get('name', ''),
        #     'about_model': {
        #         'model_title': model_data.get('title', ''),
        #         'model_about_content': model_data.get('description', ''),
        #     },
        #     'specification': {
        #         'model_configuration': model_data.get('images', []),
        #         'sleeping_area': model_data.get('sleeping_area', ''),
        #         'size': {
        #             'size_variant': {
        #                 'size_variant_length': model_data.get('length', 0),
        #                 'size_variant_depth': model_data.get('depth', 0),
        #             }
        #         },
        #         # Добавьте другие спецификации по мере необходимости
        #     },
        #     # Добавьте цвет и другие атрибуты по мере необходимости
        # }

        # # Добавляем модель в соответствующий тип
        # catalog[type_name]['model'].append(model_entry)

    except Exception as e:
        print(f"Ошибка при получении данных с {url}: {e}")

    finally:
        # Закрытие драйвера после завершения работы с текущей ссылкой
        driver.quit()

# Сохранение в файл
with open('parser/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=4)

print('------------------------------------')
print("Данные успешно сохранены в catalog.json")
print('------------------------------------')
