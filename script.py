import random

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Subject
from datacenter.models import Commendation
from datacenter.models import Lesson
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def get_schoolkid(name_schoolkid):
    try:
        if name_schoolkid and len(name_schoolkid) > 3:
            schoolkid = Schoolkid.objects.get(
                full_name__contains=name_schoolkid
            )
            return schoolkid
        else:
            print('Ошибка. Длинна имени должна быть больше 3 симв.')
    except ObjectDoesNotExist:
        print("Ошибка. Ученик не найден")
    except MultipleObjectsReturned:
        print("Ошибка. Найдено несколько учеников, вместо одного")


def get_subject(name_subject, year_of_study):
    try:
        if name_subject and len(name_subject) > 3:
            subject = Subject.objects.get(
                Q(title__contains=name_subject) &
                Q(year_of_study=year_of_study)
            )
            return subject
        else:
            print('Ошибка. Длинна назв. предмета должна быть больше 3 симв.')
    except ObjectDoesNotExist:
        print("Ошибка. Предмет не найден")
    except MultipleObjectsReturned:
        print("Ошибка. Найдено несколько предметов, вместо одного")


def get_commendation(date, schoolkid, subject, teacher):
    try:
        commendation = Commendation.objects.get(
            Q(created=date) &
            Q(schoolkid=schoolkid) &
            Q(subject=subject) &
            Q(teacher=teacher)
        )
        return commendation
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        return []


def fix_marks(name_schoolkid=''):
    schoolkid = get_schoolkid(name_schoolkid)
    if schoolkid:
        marks = Mark.objects.filter(Q(schoolkid=schoolkid) & Q(points__lt=4))
        count_of_updated = marks.update(points=5)
        if count_of_updated:
            print(f'{count_of_updated} плохих оценок заменено')
        print('Плохие оценки отсутствуют')


def remove_chastisements(name_schoolkid=''):
    schoolkid = get_schoolkid(name_schoolkid)
    if schoolkid:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        count_of_updated = chastisements.delete()[0]
        if count_of_updated:
            print(f'Удалено {count_of_updated} замечаний')
        print("Замечания отсутствуют")


def create_commendation(name_schoolkid='', name_subject=''):
    schoolkid = get_schoolkid(name_schoolkid)
    subject = schoolkid and get_subject(name_subject, schoolkid.year_of_study)
    if subject:
        lessons = Lesson.objects.filter(
            Q(year_of_study__contains=schoolkid.year_of_study) &
            Q(subject=subject) &
            Q(group_letter='А')

        )
        if lessons[0]:
            lesson_newest = lessons.order_by('-date').first()
            if get_commendation(
                    date=lesson_newest.date,
                    schoolkid=schoolkid,
                    subject=subject,
                    teacher=lesson_newest.teacher
            ) is None:
                commendation = Commendation.objects.create(
                    text=random.choice(COMMENDATIONS),
                    created=lesson_newest.date,
                    schoolkid=schoolkid,
                    subject=subject,
                    teacher=lesson_newest.teacher
                )
                print(f'Создана похвала за {commendation.created}')
            else:
                print(f'За последний урок {subject.title} уже похвали')

