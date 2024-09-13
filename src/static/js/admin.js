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