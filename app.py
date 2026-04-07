import streamlit as st
import random

st.set_page_config(
    page_title="Тренажёр: Реставрация комода",
    page_icon="🪵",
    layout="centered",
)


def generate_problem(seed: int):
    random.seed(seed)

    a = random.choice([12, 16, 20, 24, 28])
    n_top = 6
    width = a * n_top
    p_top = 4 * a

    n_mid = 4
    w_mid = width // n_mid
    h_mid = random.randint(10, a + 5)
    p_mid = 2 * (w_mid + h_mid)
    p_diff = p_mid - p_top
    s_mid = w_mid * h_mid

    h_bot = random.randint(20, 40)
    s_bot = width * h_bot
    s_diff = s_bot - s_mid
    p_bot = 2 * (width + h_bot)

    total_area = width * (a + h_mid + h_bot)

    return {
        "p_top": p_top,
        "p_diff": p_diff,
        "s_diff": s_diff,
        "correct_p_bot": p_bot,
        "correct_total_area": total_area,
        "details": {
            "width": width,
            "a": a,
            "w_mid": w_mid,
            "h_mid": h_mid,
            "h_bot": h_bot,
            "p_mid": p_mid,
            "s_mid": s_mid,
            "s_bot": s_bot,
        },
    }


def main():
    st.title("🧩 Тренажёр по геометрии: Комод")

    if "problem_idx" not in st.session_state:
        st.session_state.problem_idx = 1

    st.sidebar.header("Список задач")
    problem_numbers = list(range(1, 16))
    selected_num = st.sidebar.selectbox(
        "Выберите номер задачи",
        problem_numbers,
        index=st.session_state.problem_idx - 1,
        key="problem_select",
    )

    st.session_state.problem_idx = selected_num

    prob = generate_problem(st.session_state.problem_idx * 100)
    d = prob["details"]

    st.subheader(f"Задача №{st.session_state.problem_idx}")
    st.markdown(
        f"""
Ира реставрирует фасад старинного комода. Фасад состоит из трёх рядов ящиков:

1. **Верхний ряд** — 6 одинаковых ящиков в форме **квадрата**. Периметр одного квадрата: **{prob['p_top']} см**.
2. **Средний ряд** — 4 одинаковых прямоугольных ящика. Периметр каждого на **{abs(prob['p_diff'])} см** {'больше' if prob['p_diff'] > 0 else 'меньше'} периметра верхнего ящика.
3. **Нижний ряд** — 1 большой прямоугольный ящик. Его площадь на **{prob['s_diff']} см²** больше площади одного среднего ящика.
"""
    )

    st.divider()

    col1, col2 = st.columns(2)
    pid = st.session_state.problem_idx  # для уникальных ключей

    with col1:
        st.write("**Вопрос А:**")
        user_p = st.number_input(
            "Сколько сантиметров тесьмы нужно для отделки периметра нижнего ящика?",
            min_value=0,
            value=0,
            key=f"input_p_{pid}",
        )

    with col2:
        st.write("**Вопрос Б:**")
        user_s = st.number_input(
            "Какова общая площадь фасада комода (см²)?",
            min_value=0,
            value=0,
            key=f"input_s_{pid}",
        )

    if st.button("Проверить решение", type="primary", key=f"check_{pid}"):
        correct_p = user_p == prob["correct_p_bot"]
        correct_s = user_s == prob["correct_total_area"]

        if correct_p and correct_s:
            st.success("🎉 Великолепно! Оба ответа верны.")
            st.balloons()
        else:
            if not correct_p:
                st.error("❌ Ошибка в вопросе А. Попробуй ещё раз или раскрой подсказку.")
            if not correct_s:
                st.error("❌ Ошибка в вопросе Б. Проверь вычисления площади.")

            with st.expander("Посмотреть пошаговое решение"):
                st.markdown("**Шаги решения:**")
                st.write(f"1. Сторона квадрата: {prob['p_top']} ÷ 4 = **{d['a']} см**.")
                st.write(f"2. Ширина комода: {d['a']} × 6 = **{d['width']} см**.")
                st.write(
                    f"3. Ширина среднего ящика: {d['width']} ÷ 4 = **{d['w_mid']} см**."
                )
                st.write(
                    f"4. Периметр среднего ящика: {prob['p_top']} + ({prob['p_diff']}) = **{d['p_mid']} см**."
                )
                st.write(
                    f"5. Высота среднего ящика: ( {d['p_mid']} ÷ 2 ) − {d['w_mid']} = **{d['h_mid']} см**."
                )
                st.write(
                    f"6. Площадь среднего ящика: {d['w_mid']} × {d['h_mid']} = **{d['s_mid']} см²**."
                )
                st.write(
                    f"7. Площадь нижнего ящика: {d['s_mid']} + {prob['s_diff']} = **{d['s_bot']} см²**."
                )
                st.write(
                    f"8. Периметр нижнего ящика: 2 × ({d['width']} + {d['h_bot']}) = **{prob['correct_p_bot']} см**."
                )
                st.write(
                    f"9. Общая площадь фасада: {d['width']} × ({d['a']} + {d['h_mid']} + {d['h_bot']}) = **{prob['correct_total_area']} см²**."
                )

    st.sidebar.divider()
    st.sidebar.info("📐 Схема комода:")
    st.sidebar.markdown(
        """
<div style="border: 2px solid #5d4037; padding: 5px;">
  <div style="display: flex; gap: 2px; margin-bottom: 2px;">
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
    <div style="flex:1; height: 20px; background: #d7ccc8;"></div>
  </div>
  <div style="display: flex; gap: 2px; margin-bottom: 2px;">
    <div style="flex:1; height: 25px; background: #bcaaa4;"></div>
    <div style="flex:1; height: 25px; background: #bcaaa4;"></div>
    <div style="flex:1; height: 25px; background: #bcaaa4;"></div>
    <div style="flex:1; height: 25px; background: #bcaaa4;"></div>
  </div>
  <div style="height: 40px; background: #8d6e63;"></div>
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
