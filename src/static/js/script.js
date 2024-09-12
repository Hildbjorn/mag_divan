console.log(`
    ██████╗     ███████╗     ██████╗     Django Starter Generator -
    ██╔══██╗    ██╔════╝    ██╔════╝     приложение для автоматизации
    ██║  ██║    ███████╗    ██║  ███╗    создания, настройки и первого
    ██║  ██║    ╚════██║    ██║   ██║    запуска проектов на Django.
    ██████╔╝    ███████║    ╚██████╔╝
    ╚═════╝     ╚══════╝     ╚═════╝     Copyright (c) 2024 Artem Fomin
        `);
/*============================================*/

// Скрытие header и footer на начальной странице с оставлением menu_user
// $(document).ready(function () {
//     if (window.location.pathname === '/' || window.location.pathname === '/#') {
//         $('#header').addClass('d-none');
//         $('#header_plug').addClass('d-none');
//         $('#user_menu').removeClass('d-none');
//         $('footer').addClass('d-none');
//     } else {
//         $('#header').removeClass('d-none');
//         $('#header_plug').removeClass('d-none');
//         $('footer').removeClass('d-none');
//         $('#user_menu').addClass('d-none');
//     }
// });

// Активация ссылок
var currentLocation = window.location.pathname;
$(".navbar .nav-link").removeClass('active');
$(".nav-link[href='" + currentLocation + "']").addClass('active');

// Включение экрана со спинером загрузки
const buttons = document.querySelectorAll(".btn_submit");
const spinner = document.getElementById("spinner");
const forms = document.querySelectorAll("form");

buttons.forEach(button => {
    button.addEventListener("click", function (event) {
        let hasErrors = false;
        forms.forEach(form => {
            if (form.checkValidity() === false) {
                hasErrors = true;
                return;
            }
        });
        if (hasErrors) {
            return;
        }
        spinner.style.display = "flex";
        document.body.classList.add('lock');
    });
});

window.onload = function () {
    spinner.style.display = "none";
    document.body.classList.remove('lock');
};

// Загрузка Аватара
document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname.includes('/account')) {
        const form = document.getElementById('account_form');
        //Получаем инпут file в переменную
        const formImage = document.getElementById('avatar_field');
        //Получаем див для превью в переменную
        const formPreview = document.getElementById('avatar_preview');

        //Слушаем изменения в инпуте file
        formImage.addEventListener('change', () => {
            uploadFile(formImage.files[0]);
        });

        function uploadFile(file) {
            // проверяем тип файла
            if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
                alert('Разрешены только изображения в формате .jpeg, .png или .gif.');
                formImage.value = '';
                return;
            }
            // проверим размер файла (<5 Мб)
            if (file.size > 2 * 1024 * 1024) {
                alert('Файл должен быть менее 2 МБ.');
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                formPreview.innerHTML = `<img src="${e.target.result}" alt="Аватар">`;
            };
            reader.onerror = function (e) {
                alert('Ошибка');
            };
            reader.readAsDataURL(file);
        }
    }
});

// Автозаполнение поля "Организация"
$(document).ready(function () {
    findCompany()
});

function findCompany() {

    let companyField = document.querySelectorAll('.company_field');

    $(companyField).suggestions({
        token: "96e2dc70ca88016a7ab1e758ecd29864cd1e981d",
        type: "PARTY",
        // Вызывается, когда пользователь выбирает одну из подсказок
        onchange: function (suggestion) {
        }
    })
};

// Маска ввода номера телефона
window.addEventListener("DOMContentLoaded", function () {
    [].forEach.call(document.querySelectorAll('.tel'), function (input) {
        let keyCode;

        function mask(event) {
            event.keyCode && (keyCode = event.keyCode);
            let pos = this.selectionStart;
            if (pos < 3) event.preventDefault();
            let matrix = "+7 (___) ___ ____",
                i = 0,
                def = matrix.replace(/\D/g, ""),
                val = this.value.replace(/\D/g, ""),
                new_value = matrix.replace(/[_\d]/g, function (a) {
                    return i < val.length ? val.charAt(i++) || def.charAt(i) : a
                });
            i = new_value.indexOf("_");
            if (i != -1) {
                i < 5 && (i = 3);
                new_value = new_value.slice(0, i)
            }
            let reg = matrix.substr(0, this.value.length).replace(/_+/g,
                function (a) {
                    return "\\d{1," + a.length + "}"
                }).replace(/[+()]/g, "\\$&");
            reg = new RegExp("^" + reg + "$");
            if (!reg.test(this.value) || this.value.length < 5 || keyCode > 47 && keyCode < 58) this.value = new_value;
            if (event.type == "blur" && this.value.length < 5) this.value = ""
        }

        input.addEventListener("input", mask, false);
        input.addEventListener("focus", mask, false);
        input.addEventListener("blur", mask, false);
        input.addEventListener("keydown", mask, false)

    });
});

