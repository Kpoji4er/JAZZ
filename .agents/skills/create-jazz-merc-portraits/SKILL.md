---
name: create-jazz-merc-portraits
description: >-
  PNG-портреты мерков/NPC JAZZ в стиле JA3 (300+2000): мягкая альфа без
  агрессивного chromakey, наёмник без военных лычек, класс по киту.
  При запросе мерка/портрета/BigPortrait/field medic.
---

# Создание merc / NPC portraits

Пакет: `jazz-units` → `MercPortraits/` / `NPCPortraits/` (`_wip/` для черновиков).  
Rule: `.cursor/rules/jazz-merc-portraits.mdc`.  
Style: [references/style-and-naming.md](references/style-and-naming.md).

## Правила персонажа

- **Наёмник, не солдат:** без лычек / rank chevrons / sergeant stripes.
- Класс по киту (медик/механик/…); **оружие в кадре запрещено**.
- Полевой медик: IFAK/турникеты/shears/gauze + простой red cross — не «врач со стетоскопом».

## Альфа

1. Удачный кадр не перегенерировать.
2. Pure-black key + **смазать обводку** (blur RGB на кромке 1–2px).
3. **Не** choke / не alpha-feather-cut (зажёвывает силуэт).

## Workflow

```text
- [ ] Id / merc|NPC / роль
- [ ] Refs из MercPortraits/References/
- [ ] GenerateImage Portrait + Big (мягкая альфа в промпте, без лычек)
- [ ] Если нужно — мягкий matte, без choke
- [ ] Read: силуэт целый, cornerA=0, нет лычек
- [ ] _wip или финал; wiring по просьбе
```
