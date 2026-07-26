# Changelog JAZZ (core)

Формат ориентирован на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).  
Центральная версия релиза — из committed `metadata.lua` (`version_minor` / `version` → display `0.11-5938`, tag `v0.11.5938`).  
Публичный комплект по-прежнему требует пакеты Assets / Maps / Units.

## [0.11-5938] — 2026-07-26

Снимок `main` @ `335c19f` (+ этот changelog и сопутствующая technical-документация).

### Бой и оружие

- Мультипликативная модель стрельбы / CTH (`AccuracyRangeCTH`, связанный UI crosshair).
- Падение урона от дистанции и ребаланс оружия.
- Абилки по классам оружия (в т.ч. до боевых винтовок), правки пулемётов и миномёта.
- Трейты авто- и тяжёлого оружия; абилка «Побег с отвлечением».
- Точечные hotfix CTH/UI и particle fallback для взрывов.

### ИИ и стратегия

- Удалены сторонние AI-политики `Rato_*` из load path; зафиксирован контракт собственной AI-системы.
- Пилот глобального AI Легиона для I7 / guardpost patrols (`Guardpost_Patrols`, Regions/POI).
- Уточнены совместимость и override-матрица для strategy/AI пересечений.

### Локализация

- Исправлены ID локализации; добавлен английский перевод поверх поддержки русского.
- Контракт и skill локализации обновлены под репозиторный CSV.

### Процесс и tooling

- AI-first документация комплекта, quality gate docs, Discord-сводки изменений по push в `main`.
- Suite package gate и проверка целостности assets (`check-asset-integrity`).
- Явное одобрение перед `git push` в agent skills.
- Каталог квестов/локаций/врагов Эрни; канон боевого авто вынесен в JAZZ Maps.
- Заметки по crocodile patrol (shipping без `debug`) и smoke для `CampCrocodile_CirclingPatrol`.
- J7 «Изумрудный берег» в каталоге: `Label1=Ernie`, music Ernie_*, без `InitialSquads` (враги на карте / RescueHerMan).

### Зависимости

- Объявленная зависимость CommonLib в metadata: `version_major`/`version_minor` **1.11** (поддерживается только актуальный upstream `main`).

### Известные ограничения

- Играбельное демо — остров Эрни; материк в данных не считается поддерживаемым прохождением.
- `title` ModDef всё ещё содержит устаревшую пометку «v0.10» — номер релиза смотреть в полях metadata / этот changelog.
- Assert `goEntityPersist.cpp: cmp` на старте при Ignore обычно безопасен; Lua/runtime ошибки — нет.
- Дубликат `MapVar("gameOverState")` может дать игнорируемый assert `(not table.find(MapVars, name))`.

## [Unreleased]

Изменения после следующего Save ModDef / нового revision появятся здесь до вырезки следующего раздела.
