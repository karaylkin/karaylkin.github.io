"""
Команда для создания тестовых данных голосований.
Использование: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from polls.models import Poll, Choice, Vote


class Command(BaseCommand):
    help = 'Создает тестовые данные для голосований'

    def handle(self, *args, **options):
        # Создаем несколько голосований
        polls_data = [
            {
                'question': 'Какой язык программирования вам больше нравится?',
                'choices': ['Python', 'JavaScript', 'Java', 'C++', 'Go'],
                'votes_distribution': [45, 30, 15, 7, 3]
            },
            {
                'question': 'Какой фреймворк для веб-разработки вы предпочитаете?',
                'choices': ['Django', 'Flask', 'FastAPI', 'Tornado'],
                'votes_distribution': [50, 25, 20, 5]
            },
            {
                'question': 'Какой операционной системой вы пользуетесь?',
                'choices': ['Windows', 'Linux', 'macOS', 'Другая'],
                'votes_distribution': [40, 35, 20, 5]
            },
            {
                'question': 'Какой способ обучения вы предпочитаете?',
                'choices': ['Онлайн курсы', 'Книги', 'Видео уроки', 'Практика', 'Менторство'],
                'votes_distribution': [35, 20, 25, 15, 5]
            },
            {
                'question': 'Сколько часов в день вы программируете?',
                'choices': ['1-2 часа', '3-5 часов', '6-8 часов', 'Более 8 часов'],
                'votes_distribution': [15, 40, 30, 15]
            }
        ]

        created_count = 0
        vote_count = 0

        for i, poll_data in enumerate(polls_data):
            # Создаем голосование с датой в прошлом
            pub_date = timezone.now() - timedelta(days=random.randint(1, 30))
            poll = Poll.objects.create(
                question=poll_data['question'],
                pub_date=pub_date
            )

            # Создаем варианты ответов и голоса
            for choice_text, votes_num in zip(poll_data['choices'], poll_data['votes_distribution']):
                choice = Choice.objects.create(
                    poll=poll,
                    choice_text=choice_text
                )
                
                # Создаем голоса с распределением по времени
                for _ in range(votes_num):
                    # Голоса распределяются во времени от даты создания до сейчас
                    days_ago = random.randint(0, max(1, (timezone.now() - pub_date).days))
                    voted_at = pub_date + timedelta(days=days_ago, hours=random.randint(0, 23))
                    # Используем update_or_create чтобы установить voted_at
                    vote = Vote(choice=choice, voted_at=voted_at)
                    vote.save()
                    vote_count += 1

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Создано голосование: "{poll.question}" с {sum(poll_data["votes_distribution"])} голосами'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Успешно создано {created_count} голосований с общим количеством {vote_count} голосов'
            )
        )

