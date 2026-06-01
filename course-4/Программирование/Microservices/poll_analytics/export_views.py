"""Отдельный модуль для экспорта данных."""
from django.views import View
from django.shortcuts import get_object_or_404
from polls.models import Poll
from django.db.models import Count
from django.http import HttpResponse
import json
import csv
import io


class ExportView(View):
    """Микросервис 4: Экспорт данных в CSV и JSON."""
    
    def get(self, request, poll_id):
        """Экспортировать данные голосования."""
        poll = get_object_or_404(Poll, id=poll_id)
        format_type = request.GET.get('format', 'json').lower()
        
        # Получаем данные
        choices = poll.choice_set.annotate(annotated_vote_count=Count('votes')).all()
        total_votes = sum(choice.annotated_vote_count for choice in choices)
        
        # Подготавливаем данные для экспорта
        export_data = {
            'poll_id': poll.id,
            'question': poll.question,
            'pub_date': poll.pub_date.isoformat(),
            'total_votes': total_votes,
            'choices': []
        }
        
        for choice in choices:
            percentage = (choice.annotated_vote_count / total_votes * 100) if total_votes > 0 else 0
            export_data['choices'].append({
                'choice_text': choice.choice_text,
                'vote_count': choice.annotated_vote_count,
                'percentage': round(percentage, 2)
            })
        
        # Экспорт в CSV
        if format_type == 'csv':
            return self._export_csv(poll_id, poll, export_data, total_votes)
        
        # Экспорт в JSON (по умолчанию)
        return self._export_json(poll_id, export_data)
    
    def _export_csv(self, poll_id, poll, data, total_votes):
        """Экспорт в CSV формат."""
        output = io.StringIO()
        output.write('\ufeff')  # BOM для Excel
        
        csv_writer = csv.writer(output, delimiter=';')  # Используем точку с запятой для Excel
        
        # Заголовок отчета
        csv_writer.writerow(['ОТЧЕТ ПО ГОЛОСОВАНИЮ'])
        csv_writer.writerow(['----------------------------------------'])
        
        # Основная информация
        csv_writer.writerow(['Вопрос', poll.question])
        csv_writer.writerow(['Дата публикации', poll.pub_date.strftime('%d.%m.%Y %H:%M')])
        csv_writer.writerow(['ID голосования', poll_id])
        csv_writer.writerow(['Всего голосов', total_votes])
        
        csv_writer.writerow([])
        csv_writer.writerow(['ДЕТАЛЬНАЯ СТАТИСТИКА'])
        csv_writer.writerow(['Вариант ответа', 'Количество голосов', 'Процент (%)', 'Доля'])
        
        # Сортируем варианты по количеству голосов (от большего к меньшему)
        sorted_choices = sorted(data['choices'], key=lambda x: x['vote_count'], reverse=True)
        
        for choice in sorted_choices:
            # Визуализация доли (прогресс-бар в текстовом виде)
            bar_length = int(choice['percentage'] / 5)  # 1 символ = 5%
            bar = '█' * bar_length + '░' * (20 - bar_length)
            
            csv_writer.writerow([
                choice['choice_text'],
                choice['vote_count'],
                f"{choice['percentage']}%",
                bar
            ])
        
        # Добавляем подвал
        csv_writer.writerow([])
        csv_writer.writerow(['Сгенерировано системой аналитики', ''])

        response = HttpResponse(
            output.getvalue().encode('utf-8'),
            content_type='text/csv; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="poll_{poll_id}_statistics.csv"'
        return response
    
    def _export_json(self, poll_id, data):
        """Экспорт в JSON формат."""
        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="poll_{poll_id}_statistics.json"'
        return response


