# Phrase checklist для `$create-jazz-merc`

Статья executable, только если заполнены обязательные слоты ниже (RU + EN).

## AIM chat (обязательно)

| Слот | Кол-во |
| --- | --- |
| Offline | ≥1 |
| GreetingAndOffer | ≥1 |
| ConversationRestart | ≥1 |
| IdleLine | ≥1 |
| PartingWords | ≥1 |
| RehireIntro | ≥1 |
| RehireOutro | ≥1 |

Условно (если есть триггеры в Personality/Hire):

| Слот | Когда |
| --- | --- |
| Refusals | money / death toll / combat / disliked merc hired |
| Haggles / HaggleRehire | haggling ≠ none |
| Mitigations | liked merc hired снимает отказ |
| ExtraPartingWords | рекомендация другого мерка |

## VoiceResponse — минимум

Всегда:

- Selection
- AimAttack (≥2 варианта желательно)
- OpponentKilled
- DeathGeneral
- Downed
- CombatStartPlayer или CombatStartDetected
- LevelUp
- AmmoLow или NoAmmo
- Idle (≥1)

Если есть Likes:

- DeathBuddyN / FriendlyFireBuddyN / MockLikeN / Praises (по числу buddy)

Если есть Dislikes:

- DeathDislikeN / MockDislikeN / FriendlyFireDislikeN

## voice_source

| Значение | Фразы в статье |
| --- | --- |
| `ja2` / `ub` / `wildfire` / `nightops` | AIM chat полный draft; VR — указать «reuse legacy VO + RU subtitles draft», минимум Selection/AimAttack/OpponentKilled/DeathGeneral текстом |
| `new` | Полный минимум VR текстами |
| `reuse:<Id>` | Явный маппинг на существующий VoiceResponseId; свои AIM chat |
