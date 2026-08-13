# -*- coding: utf-8 -*-
"""
Видеоролики «Ангел-Дент» для карточки Яндекс.Бизнеса и Директа.

15 роликов собраны 29.05–08.06.2026 и лежат на Google Диске (папка
`1MxkdpkSmkKVLHgmKOiIdA8tg0Tfd7-ja`): у каждого — mp4 и постер PNG,
с которого ролик собирался. В репозиторий не тащим (≈60 МБ) и в
хранилище не перезаливаем — на странице-хабе показываем ссылками.

Запуск: python3 videos.py  → videos.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = '1MxkdpkSmkKVLHgmKOiIdA8tg0Tfd7-ja'

# номер, название, fileId ролика, fileId постера
VIDEOS = [
    ('01', 'Пенсионерам скидка 10 %', '1ki2bYx2NclFAsNiu3YXhzmZtQvZL3h-G',
     '1PVs-02Iirz1wJuZNexh1_TtGi4yo_8D-'),
    ('02', 'Чистка без боли, 5 000 ₽', '1WL_sIgrW92gcL8D-5-Z03Zap20vxgRmW',
     '1LMqcdkvcbcPfdCceDT1nFUpG13A4r3CD'),
    ('03', 'Виниры E-max', '1o4hlNklRctaeqY95upDgjXRZTjXZQqZO',
     '16_R1WpSAQZsPSjyuaxJRxpLnNdKdGXMa'),
    ('04', 'Протезирование', '1BJcNMxB9SENKDaArRGOkiD4IkxAK9IHR',
     '15VB9bOIH6_eO0j6B93MukM-Sn7sv387X'),
    ('05', 'Имплантация: 3-й имплант в подарок', '1xJdR66dxOIGPkohABSM7ot6c0Ynqj8ec',
     '1URUHk_qAEv1YG1NUvpi0ZN_kvZy78PCZ'),
    ('06', 'Чистка в подарок к имплантам и брекетам', '165l-auqjEsim0F5rODRhGdyKSLGUMnhJ',
     '1uXfT0aXjapTKsEtxnIqw8aDOlFyI-XZr'),
    ('07', 'КТ и план лечения', '1jzpg_6KpMTeTBgRm6bcubLhUa3d9Qsfg',
     '1GZR3Kcjd7-PrWGAGZ8dR5ffmnDweh95X'),
    ('08', 'Брекеты', '1AYglAPSOSD2GoCplh1pEWlRYE87NYzCS',
     '144C4DRhx7ETA9DGC0GvLHFGWyn6ZHCGn'),
    ('09', 'Отбеливание Amazing White', '1eeyVrfjeTF-CUEjchJxtlfOE2CH7mpv9',
     '1Abm1mM0Rw33doGkX1XII0DV56kgk5_qM'),
    ('10', 'Лечение кариеса', '1JNaJyDL7BZx81qxR0jHophzBwULP511F',
     '1AwkitiXM-jxmKDqnBBn_jvIwoIE4PU0A'),
    ('11', 'Удаление зуба', '1Yb6sBmNivpKWUzeC_EKhhbBTiZIp-08l',
     '1RbKYulHkT_GHgPVjEDYXbcXZmUJQ7aku'),
    ('12', 'Детская стоматология', '1rerym2bDUmgXQ16X5zNdh2YAGutMnas0',
     '1Ct34zhbOKTkrA7l1eKWDW7nqCvXNcyiv'),
    ('13', 'Лечение дёсен', '1yaP_hKZXRE2j4iyUdyjK232tcJ0NwS2u',
     '1dHAhBvDN0NMO24vyz75EUM18PAs2xrcN'),
    ('14', 'Консультация ортодонта', '1bpz-QBq3N3GLu7Y9v0KA9mj-sAh8Vvgi',
     '1VqMFI7pJnmpYFQyPv46BUO4nXWlxLwn9'),
    ('15', 'Все услуги клиники', '1MbELf5Y4zK7eoPGvUJv7RpFnP7ZwwqWZ',
     '1m0UFr7qjK55SaVSZE2s2-dnME_q4vHO0'),
]

VIEW = 'https://drive.google.com/file/d/%s/view'


def export():
    items = [{'no': no, 'title': t, 'video': VIEW % v, 'poster': VIEW % p}
             for no, t, v, p in VIDEOS]
    json.dump({'title': 'Видео', 'folder': 'https://drive.google.com/drive/folders/' + FOLDER,
               'items': items},
              open(os.path.join(HERE, 'videos.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'роликов: {len(items)}')


if __name__ == '__main__':
    export()
