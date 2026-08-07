#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AME hire-card Name/Nick Russian forms (JAZZ-UNITS-005-REQ-029).

Latin `name` stays in EN Text; RU Translation uses these nominative forms
(aligned with roster bios; genitive bio openings corrected).
"""
from __future__ import annotations

# Full formal Name (RU) keyed by English roster `name`.
AME_NAME_RU: dict[str, str] = {
    "Kwame Mensah": "Кваме Менса",
    "Jean-Baptiste Okoro": "Жан-Батист Окоро",
    "Ibrahim Touré": "Ибрахим Туре",
    "Sani Abubakar": "Сани Абубакар",
    "Pierre Ndongo": "Пьер Ндонго",
    "Moussa Diop": "Мусса Диоп",
    "Abel Getachew": "Абель Гетачью",
    "Thabo Molefe": "Табо Молефе",
    "Daniel Kiprop": "Даниэль Кипроп",
    "Emmanuel Kabongo": "Эммануэль Кабонго",
    "Aisha Hassan": "Аиша Хассан",
    "Amadou Keita": "Амаду Кейта",
    "Chidi Okonkwo": "Чиди Оконкво",
    "Lucien Mbarga": "Люсьен Мбарга",
    "Kofi Asante": "Кофи Асанте",
    "João Domingos": "Жуан Домингос",
    "Wanjiku Mwangi": "Ванджику Мванги",
    "Serge Kouassi": "Серж Куасси",
    "Bongani Dlamini": "Бонгани Дламини",
    "Idrissa Bah": "Идрисса Бах",
    "Omar Diallo": "Омар Диалло",
    "Bastien Lafontaine": "Бастьен Лафонтен",
    "Chukwuemeka Obi": "Чуквуэмека Оби",
    "Michel Kabeya": "Мишель Кабея",
    "Juma Otieno": "Джума Отиено",
    "Andile Nkosi": "Андиле Нкоси",
    "Sekou Camara": "Секу Камара",
    "Pascal Ngoma": "Паскаль Нгома",
    "Kwesi Boateng": "Квеси Боатенг",
    "Tesfaye Alemu": "Тесфайе Алему",
    "Rafael dos Santos": "Рафаэль дос Сантос",
    "Awa Sow": "Ава Соу",
    "Claude Mvemba": "Клод Мвемба",
    "Emeka Nwosu": "Эмека Нвосу",
    "Samuel Cheruiyot": "Сэмюэл Черуйот",
    "Mamadou Traoré": "Мамаду Траоре",
    "Felix Tshisekedi": "Феликс Чисекеди",
    "Noah van Wyk": "Ноа ван Вейк",
    "Joseph Mukendi": "Жозеф Мукенди",
    "Abraham Tekle": "Абрахам Текле",
    "Sipho Khumalo": "Сифо Кхумало",
    "Boubacar Kane": "Бубакар Кане",
    "Didier Mbemba": "Дидье Мбемба",
    "Amina Yusuf": "Амина Юсуф",
    "Léopold Sassou": "Леопольд Сассу",
    "Kofi Mensah": "Кофи Менса",
    "Hassan Ibrahim": "Хассан Ибрахим",
    "Patrick Omondi": "Патрик Омонди",
    "Dr. Fatoumata Sy": "Доктор Фатумата Си",
    "Grace Wanjiru": "Грейс Ванджиру",
    "Dr. Emile Kabongo": "Доктор Эмиль Кабонго",
    "Captain Amara Koné": "Капитан Амара Коне",
    "Sgt. Nadia Okonkwo": "Сержант Надия Оконкво",
    "Maj. Théodore Ngalula": "Майор Теодор Нгалула",
    "Issa Camara": "Исса Камара",
    "Lindiwe Mokoena": "Линдиве Мокоена",
    "Bakary Diarra": "Бакари Диарра",
    "Marie-Claire Mbala": "Мари-Клер Мбала",
    "Ousmane Fall": "Усман Фалл",
    "Jean-Pierre Kalala": "Жан-Пьер Калала",
}

# Explicit English nick → RU (Hardened callsigns + short forms).
AME_NICK_RU: dict[str, str] = {
    "Emeka": "Эмека",
    "Hyena": "Гиена",
    "Anvil": "Анвил",  # short callsign; «Наковальня» не влезает в тайл
    "Smoke": "Дым",
    "Scorpion": "Скорпион",
}
