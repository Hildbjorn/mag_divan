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

/*=========================================================================*/
// Активация ссылок
/*=========================================================================*/
var currentLocation = window.location.pathname;
var navLinks = $(".navbar .nav-link");

if (navLinks.length) { // Проверка наличия .nav-link
    navLinks.removeClass('active');
    navLinks.filter("[href='" + currentLocation + "']").addClass('active');
}

/*=========================================================================*/
// Включение экрана со спинером загрузки
/*=========================================================================*/
const buttons = document.querySelectorAll(".btn_submit");
const spinner = document.getElementById("spinner");
const forms = document.querySelectorAll("form");

// Проверка наличия кнопок и спиннера
if (buttons.length > 0 && spinner) {
    buttons.forEach(button => {
        button.addEventListener("click", function (event) {
            let hasErrors = false;

            // Проверка наличия форм
            if (forms.length > 0) {
                forms.forEach(form => {
                    if (form.checkValidity() === false) {
                        hasErrors = true;
                        return;
                    }
                });
            }

            if (hasErrors) {
                return;
            }

            spinner.style.display = "flex";
            document.body.classList.add('lock');
        });
    });
}

window.onload = function () {
    spinner.style.display = "none";
    document.body.classList.remove('lock');
};


/*=========================================================================*/
// Загрузка Аватара
/*=========================================================================*/
document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname.includes('/account')) {
        const form = document.getElementById('account_form');
        const formImage = document.getElementById('avatar_field');
        const formPreview = document.getElementById('avatar_preview');

        // Проверка наличия элементов
        if (!formImage || !formPreview) {
            return;
        }

        // Слушаем изменения в инпуте file
        formImage.addEventListener('change', () => {
            uploadFile(formImage.files[0]);
        });

        function uploadFile(file) {
            // Проверяем тип файла
            if (!file) {
                alert('Пожалуйста, выберите файл.');
                return;
            }

            if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
                alert('Разрешены только изображения в формате .jpeg, .png или .gif.');
                formImage.value = '';
                return;
            }

            // Проверяем размер файла (<2 Мб)
            if (file.size > 2 * 1024 * 1024) {
                alert('Файл должен быть менее 2 МБ.');
                formImage.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                formPreview.innerHTML = `<img src="${e.target.result}" alt="Аватар" style="max-width: 100%; height: auto;">`;
            };
            reader.onerror = function () {
                alert('Ошибка при чтении файла. Попробуйте еще раз.');
            };
            reader.readAsDataURL(file);
        }
    }
});

/*=========================================================================*/
// Автозаполнение поля "Организация"
/*=========================================================================*/
$(document).ready(function () {
    findCompany();
});

function findCompany() {
    let companyField = document.querySelectorAll('.company_field');

    // Проверяем, найдены ли элементы
    if (companyField.length === 0) {
        return; // Выходим из функции, если элементы не найдены
    }

    $(companyField).suggestions({
        token: "96e2dc70ca88016a7ab1e758ecd29864cd1e981d",
        type: "PARTY",
        // Вызывается, когда пользователь выбирает одну из подсказок
        onchange: function (suggestion) {
            // Обработка выбора подсказки
        }
    });
}
/*=========================================================================*/
// Маска ввода номера телефона
/*=========================================================================*/
window.addEventListener("DOMContentLoaded", function () {
    let telInputs = document.querySelectorAll('.tel');

    // Проверяем, найдены ли элементы
    if (telInputs.length === 0) {
        return; // Выходим из функции, если элементы не найдены
    }

    [].forEach.call(telInputs, function (input) {
        let keyCode;

        function mask(event) {
            event.keyCode && (keyCode = event.keyCode);
            let pos = this.selectionStart;
            if (pos < 3) event.preventDefault();
            let matrix = "+7 (____) ____ _____",
                i = 0,
                def = matrix.replace(/\D/g, ""),
                val = this.value.replace(/\D/g, ""),
                new_value = matrix.replace(/[_\d]/g, function (a) {
                    return i < val.length ? val.charAt(i++) : def.charAt(i);
                });
            i = new_value.indexOf("_");
            if (i != -1) {
                i < 5 && (i = 3);
                new_value = new_value.slice(0, i);
            }
            let reg = matrix.substr(0, this.value.length).replace(/_+/g,
                function (a) {
                    return "\\d{1," + a.length + "}";
                }).replace(/[+()]/g, "\\$&");
            reg = new RegExp("^" + reg + "$");
            if (!reg.test(this.value) || this.value.length < 5 || (keyCode > 47 && keyCode < 58)) {
                this.value = new_value;
            }
            if (event.type == "blur" && this.value.length < 5) this.value = "";
        }

        input.addEventListener("input", mask, false);
        input.addEventListener("focus", mask, false);
        input.addEventListener("blur", mask, false);
        input.addEventListener("keydown", mask, false);
    });
});

