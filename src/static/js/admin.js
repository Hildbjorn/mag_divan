console.log(`
    ██████╗     ███████╗     ██████╗     Django Starter Generator -
    ██╔══██╗    ██╔════╝    ██╔════╝     приложение для автоматизации
    ██║  ██║    ███████╗    ██║  ███╗    создания, настройки и первого
    ██║  ██║    ╚════██║    ██║   ██║    запуска проектов на Django.
    ██████╔╝    ███████║    ╚██████╔╝
    ╚═════╝     ╚══════╝     ╚═════╝     Copyright (c) 2024 Artem Fomin
        `);
/*============================================*/
// Показ изображения в админке
document.addEventListener('DOMContentLoaded', function () {
    // Проверяем наличие <fieldset class="module aligned ">
    const fieldset = document.querySelector('fieldset.module.aligned');

    if (fieldset) {
        console.log("Скрипт предпросмотра запущен");
        const imageInput = document.querySelector('input[type="file"][name="image"]');
        const thumbnail = document.getElementById('image_thumbnail');
        if (imageInput && thumbnail) {
            imageInput.addEventListener('change', function (event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        thumbnail.src = e.target.result;
                    }
                    reader.readAsDataURL(file);
                }
            });
        }
    }
});

// Замена label на кружок с описанием
document.addEventListener("DOMContentLoaded", function () {
    // Проверяем, есть ли на странице div с классом id_colors
    const colorDiv = document.querySelector('.id_colors');

    if (colorDiv) {
        // Получаем все checkbox внутри этого div
        const checkboxes = colorDiv.querySelectorAll('input[type="checkbox"]');

        checkboxes.forEach(function (checkbox) {
            // Находим соответствующий label для каждого checkbox
            const label = document.querySelector(`label[for= "${checkbox.id}"]`);

            if (label) {
                // Здесь вы можете заменить {color.hex_code} и {color.name} на реальные значения
                const color = {
                    hex_code: '#ff5733', // Пример цвета
                    name: 'Красный'      // Пример имени цвета
                };

                // Создаем новый HTML для label
                label.innerHTML =
                    `<div class="display_colors_item">
                    <div class="display_colors_sample" style="background-color: ${color.hex_code};"></div>
                    <span>${color.name} (${color.hex_code})</span>
                </div>`;
            }
        });
    }
});



// Показ только тех цветов, которые связаны с моделью
document.addEventListener('DOMContentLoaded', function () {
    const furnitureModelSelect = document.getElementById('id_furniture_model');
    const colorsSelect = document.getElementById('id_color');
    const fieldColorDiv = document.querySelector('.field-color'); // Получаем элемент с классом .field-color

    // Проверяем наличие необходимых элементов
    if (!furnitureModelSelect || !colorsSelect || !fieldColorDiv) {
        console.error('Не все необходимые элементы найдены на странице.');
        return; // Прерываем выполнение, если элементы отсутствуют
    }

Функция для обновления списка цветов
    function updateColorOptions(colors) {
        colorsSelect.innerHTML = ''; // Очищаем текущее содержимое

        colors.forEach(color => {
            const option = new Option(color.name, color.id);
            colorsSelect.add(option);
        });
    }

    // Функция для получения всех цветов
    function fetchAllColors() {
        fetch(`/catalog/admin/get_all_colors/`)
            .then(response => response.json())
            .then(data => {
                updateColorOptions(data.colors);
            })
            .catch(error => console.error('Error fetching all colors:', error));
    }

    function slideUp(element) {
        element.classList.remove('active');
        setTimeout(() => {
            element.style.display = 'none'; // Скрываем элемент после завершения анимации
        }, 500); // Время должно совпадать с длительностью transition
    }

    function slideDown(element) {
        element.style.display = 'block'; // Сначала показываем элемент
        setTimeout(() => {
            element.classList.add('active'); // Затем добавляем класс для анимации
        }, 10); // Небольшая задержка для активации transition
    }

    furnitureModelSelect.addEventListener('change', function () {
        const modelId = this.value;

        if (modelId) {
            slideDown(fieldColorDiv); // Показываем элемент, если модель выбрана

            // Получаем цвета для выбранной модели через AJAX
            fetch(`/catalog/admin/get_colors/${modelId}/`)
                .then(response => response.json())
                .then(data => {
                    updateColorOptions(data.colors);
                })
                .catch(error => console.error('Error fetching colors:', error));
        } else {
            slideUp(fieldColorDiv); // Скрываем элемент, если модель не выбрана
            fetchAllColors();
        }
    });
});




