from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'

# Меню шаурмичной
menu_items = [
    {'id': 1, 'name': 'Классическая с курицей', 'category': 'classic', 'price': 250, 'weight': '350г',
     'description': 'Курица, овощи, соус в лаваше'},
    {'id': 2, 'name': 'С говядиной', 'category': 'classic', 'price': 320, 'weight': '380г',
     'description': 'Говядина, томаты, лук, чесночный соус'},
    {'id': 3, 'name': 'Острая', 'category': 'spicy', 'price': 280, 'weight': '360г',
     'description': 'Курица, перец халапеньо, острый соус'},
    {'id': 4, 'name': 'Картошка фри', 'category': 'sides', 'price': 120, 'weight': '150г',
     'description': 'Хрустящая картошка со специями'},
    {'id': 5, 'name': 'Кола 0.5л', 'category': 'drinks', 'price': 90, 'weight': '500мл',
     'description': 'Газированный напиток'},
]

# Хранилище промокодов
student_promos = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    # Параметр запроса для фильтрации
    category = request.args.get('category', type=str)

    if category:
        filtered_items = [item for item in menu_items if item['category'] == category]
    else:
        filtered_items = menu_items

    return render_template("menu.html", items=filtered_items, current_category=category)


@app.route("/menu/<int:id>")
def dish(id):
    # Параметр маршрута
    dish_item = next((item for item in menu_items if item['id'] == id), None)

    if dish_item is None:
        flash('Блюдо не найдено', 'error')
        return redirect(url_for('menu'))

    return render_template("dish.html", dish=dish_item)


@app.route("/promo", methods=['GET', 'POST'])
def promo():
    if request.method == 'POST':
        # Получение данных из формы
        full_name = request.form.get('full_name', '').strip()
        university = request.form.get('university', '').strip()
        student_id = request.form.get('student_id', '').strip()

        # Валидация
        errors = {}

        if not full_name or len(full_name) < 5:
            errors['full_name'] = 'Введите полное ФИО (минимум 5 символов)'

        if not university or len(university) < 3:
            errors['university'] = 'Укажите название учебного заведения'

        if not student_id or len(student_id) < 5:
            errors['student_id'] = 'Введите корректный номер студенческого билета'

        # Проверка, не получал ли уже промокод
        already_used = any(p['student_id'] == student_id for p in student_promos)
        if already_used:
            errors['student_id'] = 'Промокод для этого студенческого уже был выдан'

        if not errors:
            # Генерируем промокод
            promo_code = 'STUDENT-' + student_id[-4:].upper() + '-15'

            new_promo = {
                'full_name': full_name,
                'university': university,
                'student_id': student_id,
                'code': promo_code
            }
            student_promos.append(new_promo)

            # Передача данных в шаблон
            return render_template("promo.html",
                                   errors={},
                                   form_data={},
                                   promo_code=promo_code)

        return render_template("promo.html",
                               errors=errors,
                               form_data={'full_name': full_name, 'university': university, 'student_id': student_id})

    return render_template("promo.html", errors={}, form_data={})


@app.route("/order")
def order():
    return render_template("order.html")


@app.route("/changelog")
def changelog():
    return render_template("changelog.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)