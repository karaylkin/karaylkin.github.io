import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Настройки стиля
sns.set_style("whitegrid")
# Попытка установить шрифт, поддерживающий кириллицу. 
# Если DejaVu Sans нет, matplotlib может использовать дефолтный, который может не отображать кириллицу корректно.
# В Windows часто работает Arial или Segoe UI.
try:
    plt.rcParams['font.family'] = 'DejaVu Sans'
except:
    plt.rcParams['font.family'] = 'Arial'

plt.rcParams['figure.dpi'] = 100

# ============================================
# ГЕНЕРАЦИЯ ДАННЫХ
# ============================================

# Создание тестовых данных
np.random.seed(42)
n_students = 25

students = [f'Ученик_{i}' for i in range(1, n_students + 1)]
subjects = ['Математика', 'Русский', 'Физика', 'Информатика', 'История']

# Генерация оценок
data = {'Ученик': students}
for subject in subjects:
    data[subject] = np.random.randint(3, 6, n_students)

df = pd.DataFrame(data)
df['Средний_балл'] = df[subjects].mean(axis=1).round(2)

# Данные по четвертям для динамики
quarters_data = pd.DataFrame({
    'Четверть': ['1 четв.', '2 четв.', '3 четв.', '4 четв.'],
    'Средний_балл': [3.9, 4.0, 4.2, 4.3]
})

# ============================================
# СОЗДАНИЕ ДАШБОРДА
# ============================================

fig = plt.figure(figsize=(20, 12))
fig.suptitle('ДАШБОРД УСПЕВАЕМОСТИ КЛАССА', 
             fontsize=24, fontweight='bold', y=0.98)

# 1. Средние баллы по предметам
ax1 = plt.subplot(3, 3, 1)
subject_means = df[subjects].mean().sort_values(ascending=False)
colors = plt.cm.viridis(np.linspace(0, 1, len(subjects)))
bars = ax1.bar(range(len(subjects)), subject_means.values, color=colors, edgecolor='black')
ax1.set_xticks(range(len(subjects)))
ax1.set_xticklabels(subject_means.index, rotation=45, ha='right')
ax1.set_ylabel('Средний балл', fontsize=11, fontweight='bold')
ax1.set_title('Средние баллы по предметам', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 5.5) # Немного увеличим лимит для текста
ax1.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# 2. Распределение оценок
ax2 = plt.subplot(3, 3, 2)
all_grades = pd.concat([df[subject] for subject in subjects])
grade_counts = all_grades.value_counts().sort_index()
colors_pie = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
# Убедимся, что цветов хватает (если оценок меньше 4 типов)
current_colors = colors_pie[:len(grade_counts)]
explode = [0.05] * len(grade_counts)

ax2.pie(grade_counts.values, labels=[f'{int(g)}' for g in grade_counts.index],
        colors=current_colors, autopct='%1.1f%%', startangle=90, explode=explode,
        textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('Распределение оценок', fontsize=12, fontweight='bold')

# 3. Топ-10 учеников
ax3 = plt.subplot(3, 3, 3)
top10 = df.nlargest(10, 'Средний_балл')[['Ученик', 'Средний_балл']]
top10 = top10.sort_values('Средний_балл', ascending=True) # Сортируем для barh (снизу вверх)
colors_top = plt.cm.RdYlGn(np.linspace(0.3, 1, len(top10)))
ax3.barh(range(len(top10)), top10['Средний_балл'].values, color=colors_top, edgecolor='black')

ax3.set_yticks(range(len(top10)))
ax3.set_yticklabels(top10['Ученик'].values, fontsize=9)
ax3.set_xlabel('Средний балл', fontsize=11, fontweight='bold')
ax3.set_title('Топ-10 лучших учеников', fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)
ax3.set_xlim(0, 5.5)
for i, v in enumerate(top10['Средний_балл'].values):
    ax3.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold', fontsize=9)

# 4. Тепловая карта
# Используем subplot2grid для размещения на всю ширину второго ряда
ax4 = plt.subplot2grid((3, 3), (1, 0), colspan=3)

heatmap_data = df.set_index('Ученик')[subjects]
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn', 
            vmin=2, vmax=5, cbar_kws={'label': 'Оценка'},
            linewidths=0.5, linecolor='gray', ax=ax4)
ax4.set_title('Оценки учеников по предметам', fontsize=12, fontweight='bold')
ax4.set_ylabel('Ученик', fontsize=11, fontweight='bold')
ax4.set_xlabel('Предмет', fontsize=11, fontweight='bold')

# 5. Динамика успеваемости
ax5 = plt.subplot(3, 3, 7)
ax5.plot(quarters_data['Четверть'], quarters_data['Средний_балл'],
         marker='o', linewidth=3, markersize=12, color='#3498db')
ax5.set_ylabel('Средний балл класса', fontsize=11, fontweight='bold')
ax5.set_title('Динамика успеваемости по четвертям', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.set_ylim(3.5, 4.5)
for i, row in quarters_data.iterrows():
    ax5.text(i, row['Средний_балл'] + 0.05, f"{row['Средний_балл']:.1f}",
             ha='center', fontweight='bold', fontsize=10)

# 6. Box plot по предметам
ax6 = plt.subplot(3, 3, 8)
df_melted = df[subjects].melt(var_name='Предмет', value_name='Балл')
sns.boxplot(x='Предмет', y='Балл', data=df_melted, palette='Set2', ax=ax6)
ax6.set_title('Разброс оценок по предметам', fontsize=12, fontweight='bold')
ax6.set_xlabel('Предмет', fontsize=11, fontweight='bold')
ax6.set_ylabel('Балл', fontsize=11, fontweight='bold')
ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
ax6.grid(axis='y', alpha=0.3)

# 7. Статистика класса
ax7 = plt.subplot(3, 3, 9)
ax7.axis('off')

stats = {
    'Всего учеников': len(df),
    'Средний балл': df['Средний_балл'].mean(),
    'Медиана': df['Средний_балл'].median(),
    'Отличников (≥4.5)': len(df[df['Средний_балл'] >= 4.5]),
    'Хорошистов (≥3.5)': len(df[(df['Средний_балл'] >= 3.5) & (df['Средний_балл'] < 4.5)]),
    'Троечников (<3.5)': len(df[df['Средний_балл'] < 3.5])
}

best_subject = subject_means.idxmax()
worst_subject = subject_means.idxmin()

stats_text = f"""
{'='*35}
   СТАТИСТИКА КЛАССА
{'='*35}

Всего учеников: {stats['Всего учеников']}

Средний балл: {stats['Средний балл']:.2f}
Медиана: {stats['Медиана']:.2f}

РАСПРЕДЕЛЕНИЕ:
  Отличников: {stats['Отличников (≥4.5)']} ({stats['Отличников (≥4.5)']/stats['Всего учеников']*100:.0f}%)
  Хорошистов: {stats['Хорошистов (≥3.5)']} ({stats['Хорошистов (≥3.5)']/stats['Всего учеников']*100:.0f}%)
  Троечников: {stats['Троечников (<3.5)']} ({stats['Троечников (<3.5)']/stats['Всего учеников']*100:.0f}%)

ПРЕДМЕТЫ:
  Лучший: {best_subject}
           ({subject_means[best_subject]:.2f})
  Сложный: {worst_subject}
           ({subject_means[worst_subject]:.2f})

Дата: {datetime.now().strftime('%d.%m.%Y')}
{'='*35}
"""

ax7.text(0.05, 0.95, stats_text, transform=ax7.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, pad=1))

# Сохранение
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'dashboard.png')

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Дашборд сохранён в {output_path}")

# Показываем график (если есть GUI)
try:
    plt.show()
except:
    pass
