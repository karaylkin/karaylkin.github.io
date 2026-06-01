import pandas as pd
import numpy as np
from datetime import datetime
import os

# ============================================
# ЗАГРУЗКА И ПОДГОТОВКА ДАННЫХ
# ============================================

def load_journal(filename='journal.csv'):
    """Загрузка журнала из файла"""
    # Получаем абсолютный путь к папке, где лежит этот скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Собираем полный путь к файлу данных
    file_path = os.path.join(script_dir, filename)

    try:
        if not os.path.exists(file_path):
            print(f"❌ Файл {filename} не найден по пути: {file_path}")
            return None
            
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"✅ Данные успешно загружены из {filename}")
        print(f"   Количество учеников: {len(df)}")
        return df
    except Exception as e:
        print(f"❌ Ошибка при загрузке файла: {e}")
        return None

# ============================================
# АНАЛИЗ ДАННЫХ
# ============================================

def calculate_statistics(df):
    """Расчёт статистики по журналу"""
    
    # Определяем столбцы с предметами (все кроме 'Ученик')
    subject_columns = [col for col in df.columns if col != 'Ученик']
    
    # Расчёт среднего балла каждого ученика
    df['Средний_балл'] = df[subject_columns].mean(axis=1).round(2)
    
    # Определение статуса
    def get_status(avg):
        if avg >= 4.5:
            return 'Отличник'
        elif avg >= 3.5:
            return 'Хорошист'
        elif avg >= 2.5:
            return 'Троечник'
        else:
            return 'Требует внимания'
    
    df['Статус'] = df['Средний_балл'].apply(get_status)
    
    return df, subject_columns

def get_class_statistics(df, subject_columns):
    """Получение общей статистики класса"""
    
    stats = {
        'total_students': len(df),
        'class_average': df['Средний_балл'].mean(),
        'class_median': df['Средний_балл'].median(),
        'class_std': df['Средний_балл'].std(),
        'class_min': df['Средний_балл'].min(),
        'class_max': df['Средний_балл'].max(),
        'excellent': len(df[df['Статус'] == 'Отличник']),
        'good': len(df[df['Статус'] == 'Хорошист']),
        'satisfactory': len(df[df['Статус'] == 'Троечник']),
        'attention_needed': len(df[df['Статус'] == 'Требует внимания'])
    }
    
    return stats

def get_subject_statistics(df, subject_columns):
    """Статистика по каждому предмету"""
    
    subject_stats = {}
    for subject in subject_columns:
        subject_stats[subject] = {
            'mean': df[subject].mean(),
            'median': df[subject].median(),
            'std': df[subject].std(),
            'min': df[subject].min(),
            'max': df[subject].max()
        }
    
    return subject_stats

# ============================================
# ВЫЯВЛЕНИЕ ГРУПП УЧЕНИКОВ
# ============================================

def get_top_students(df, n=5):
    """Топ-N лучших учеников"""
    return df.nlargest(n, 'Средний_балл')[['Ученик', 'Средний_балл', 'Статус']]

def get_struggling_students(df, threshold=3.5):
    """Ученики, требующие внимания"""
    return df[df['Средний_балл'] < threshold][['Ученик', 'Средний_балл', 'Статус']]

# ============================================
# ФОРМИРОВАНИЕ ОТЧЁТА
# ============================================

def create_text_report(df, stats, subject_stats, filename='report.txt'):
    """Создание текстового отчёта"""
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ОТЧЁТ ПО УСПЕВАЕМОСТИ КЛАССА\n")
            f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Общая статистика
            f.write("ОБЩАЯ СТАТИСТИКА КЛАССА\n")
            f.write("-" * 80 + "\n")
            f.write(f"Всего учеников: {stats['total_students']}\n")
            f.write(f"Средний балл класса: {stats['class_average']:.2f}\n")
            f.write(f"Медиана: {stats['class_median']:.2f}\n")
            f.write(f"Стандартное отклонение: {stats['class_std']:.2f}\n")
            f.write(f"Минимальный балл: {stats['class_min']:.2f}\n")
            f.write(f"Максимальный балл: {stats['class_max']:.2f}\n\n")
            
            # Распределение по категориям
            f.write("РАСПРЕДЕЛЕНИЕ УЧЕНИКОВ\n")
            f.write("-" * 80 + "\n")
            total = stats['total_students']
            f.write(f"Отличников: {stats['excellent']} ({stats['excellent']/total*100:.1f}%)\n")
            f.write(f"Хорошистов: {stats['good']} ({stats['good']/total*100:.1f}%)\n")
            f.write(f"Троечников: {stats['satisfactory']} ({stats['satisfactory']/total*100:.1f}%)\n")
            f.write(f"Требуют внимания: {stats['attention_needed']} ({stats['attention_needed']/total*100:.1f}%)\n\n")
            
            # Статистика по предметам
            f.write("СТАТИСТИКА ПО ПРЕДМЕТАМ\n")
            f.write("-" * 80 + "\n")
            for subject, subject_stat in subject_stats.items():
                f.write(f"\n{subject}:\n")
                f.write(f"  Средний балл: {subject_stat['mean']:.2f}\n")
                f.write(f"  Медиана: {subject_stat['median']:.2f}\n")
                f.write(f"  Стд. отклонение: {subject_stat['std']:.2f}\n")
                f.write(f"  Мин/Макс: {subject_stat['min']:.0f} / {subject_stat['max']:.0f}\n")
            
            # Топ-5 учеников
            f.write("\n" + "=" * 80 + "\n")
            f.write("ТОП-5 ЛУЧШИХ УЧЕНИКОВ\n")
            f.write("-" * 80 + "\n")
            top = get_top_students(df, 5)
            for i, (_, row) in enumerate(top.iterrows(), 1):
                f.write(f"{i}. {row['Ученик']}: {row['Средний_балл']:.2f} ({row['Статус']})\n")
            
            # Ученики, требующие внимания
            struggling = get_struggling_students(df)
            if len(struggling) > 0:
                f.write("\n" + "=" * 80 + "\n")
                f.write("⚠️  УЧЕНИКИ, ТРЕБУЮЩИЕ ВНИМАНИЯ\n")
                f.write("-" * 80 + "\n")
                for _, row in struggling.iterrows():
                    f.write(f"  • {row['Ученик']}: {row['Средний_балл']:.2f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("Конец отчёта\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Текстовый отчёт сохранён в {filename}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении отчета: {e}")

# ============================================
# СОХРАНЕНИЕ В EXCEL
# ============================================

def save_to_excel(df, filename='journal_analysis.xlsx'):
    """Сохранение результатов в Excel с форматированием"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Лист 1: Полные данные
            df_sorted = df.sort_values('Средний_балл', ascending=False)
            df_sorted.to_excel(writer, sheet_name='Полный журнал', index=False)
            
            # Лист 2: Отличники и хорошисты
            best = df[df['Статус'].isin(['Отличник', 'Хорошист'])].sort_values('Средний_балл', ascending=False)
            best.to_excel(writer, sheet_name='Отличники и хорошисты', index=False)
            
            # Лист 3: Требуют внимания
            struggling = df[df['Средний_балл'] < 3.5].sort_values('Средний_балл')
            if len(struggling) > 0:
                struggling.to_excel(writer, sheet_name='Требуют внимания', index=False)
        
        print(f"✅ Результаты сохранены в {filename}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении Excel (возможно, не установлен openpyxl): {e}")

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    """Основная функция программы"""
    
    print("\n" + "=" * 80)
    print("СИСТЕМА АНАЛИЗА УСПЕВАЕМОСТИ")
    print("=" * 80 + "\n")
    
    # 1. Загрузка данных
    df = load_journal('journal.csv')
    if df is None:
        return
    
    # 2. Расчёт статистики
    print("\n📊 Обработка данных...")
    df, subject_columns = calculate_statistics(df)
    
    # 3. Получение статистики
    stats = get_class_statistics(df, subject_columns)
    subject_stats = get_subject_statistics(df, subject_columns)
    
    # 4. Вывод результатов в консоль
    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 80)
    
    print(f"\n📈 Средний балл класса: {stats['class_average']:.2f}")
    print(f"📊 Медиана: {stats['class_median']:.2f}")
    
    print(f"\n👥 Распределение учеников:")
    print(f"   Отличников: {stats['excellent']}")
    print(f"   Хорошистов: {stats['good']}")
    print(f"   Троечников: {stats['satisfactory']}")
    print(f"   Требуют внимания: {stats['attention_needed']}")
    
    print("\n🏆 ТОП-5 ЛУЧШИХ УЧЕНИКОВ:")
    top = get_top_students(df, 5)
    for i, (_, row) in enumerate(top.iterrows(), 1):
        print(f"   {i}. {row['Ученик']}: {row['Средний_балл']:.2f}")
    
    # 5. Сохранение результатов
    print("\n💾 Сохранение результатов...")
    save_to_excel(df, 'journal_analysis.xlsx')
    create_text_report(df, stats, subject_stats, 'report.txt')
    
    print("\n✅ Анализ завершён!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()