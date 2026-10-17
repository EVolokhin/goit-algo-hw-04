import turtle

def koch_curve(t, length, order):
    """Рекурсивна функція для малювання кривої Коха."""
    if order == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_curve(t, length, order - 1)
        t.left(60)
        koch_curve(t, length, order - 1)
        t.right(120)
        koch_curve(t, length, order - 1)
        t.left(60)
        koch_curve(t, length, order - 1)

def draw_koch_snowflake(order, length=300):
    """Налаштування вікна та малювання повної сніжинки Коха."""
    # Налаштування вікна
    window = turtle.Screen()
    window.title("Фрактал «Сніжинка Коха»")
    window.bgcolor("white")

    # Налаштування черепашки
    t = turtle.Turtle()
    t.speed(0)  # Максимальна швидкість малювання
    t.color("blue")
    t.pensize(2)

    # Початкове позиціонування черепашки по центру екрана
    t.penup()
    t.goto(-length / 2, length / 3)
    t.pendown()

    # Сніжинка Коха складається з трьох кривих Коха, розташованих у вигляді трикутника
    for _ in range(3):
        koch_curve(t, length, order)
        t.right(120)

    t.hideturtle()
    window.mainloop()

def main():
    try:
        # Отримуємо рівень рекурсії від користувача
        user_input = input("Введіть рівень рекурсії для сніжинки Коха (рекомендовано від 0 до 4): ")
        level = int(user_input)
        
        if level < 0:
            print("Помилка: рівень рекурсії не може бути від'ємним числом.")
            return

        print(f"Малюємо сніжинку Коха з рівнем рекурсії {level}...")
        draw_koch_snowflake(level)

    except ValueError:
        print("Помилка: будь ласка, введіть ціле число.")

if __name__ == "__main__":
    main()