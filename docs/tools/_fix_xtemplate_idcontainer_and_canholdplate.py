#!/usr/bin/env python3
"""Fix SquadsAndMercs nested idContainer and boolean armor rollover binds in items.lua."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / "items.lua"
text = path.read_text(encoding="utf-8")
orig = text
lines = text.splitlines(keepends=True)

xt_id = None
out = []
removed = 0
i = 0
while i < len(lines):
	line = lines[i]
	s = line.strip()
	if s.startswith("PlaceObj('ModItemXTemplate'"):
		xt_id = None
	if xt_id is None and s.startswith("id =") and '"SquadsAndMercs' in s:
		xt_id = s.split('"')[1]
	if (
		xt_id == "SquadsAndMercs"
		and "'Id', \"idContainer\"" in line
		and (len(line) - len(line.lstrip("\t"))) >= 9
	):
		removed += 1
		i += 1
		continue
	out.append(line)
	i += 1

text = "".join(out)

old_plate = """						PlaceObj('XTemplateTemplate', {
							'comment', "Canholdplate",
							'__condition', function (parent, context) local cnt = ResolvePropObj(context); return  IsKindOf(cnt, "Armor") and (cnt.Slot == "Torso" or not  cnt.Slot) and cnt.CanHoldPlate end,
							'__template', "RolloverPropTextRight",
							'OnLayoutComplete', function (self)
								self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
								self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
							end,
							'BindTo', "CanHoldPlate",
							'Text', T(724608997137, --[[ModItemXTemplate RolloverInventoryWeaponBase Text]] "Уровень защиты"),
							'PercentValue', true,
						}, {
							PlaceObj('XTemplateFunc', {
								'name', "Open(self,...)",
								'func', function (self,...)
									self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
									self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
									XPropControl.Open(self,...)
									
									
									local cnt = ResolvePropObj(self.context);
									--if cnt.CanHoldPlate == true 
									--	then 
									--		self.idPropVal:SetValueText(T{54113904164711288, "Да"})
									--	else
									--		self.idPropVal:SetValueText(T{54113904164711288, "Нет"})
									--end
									self.idPropVal:SetValueText("")
									self.idPropVal:SetNameText(T(890000000001415, "Возможность установки плиты"))
								end,
							}),
							}),"""

new_plate = """						PlaceObj('XTemplateTemplate', {
							'comment', "Canholdplate",
							'__condition', function (parent, context) local cnt = ResolvePropObj(context); return  IsKindOf(cnt, "Armor") and (cnt.Slot == "Torso" or not  cnt.Slot) and cnt.CanHoldPlate end,
							'__template', "RolloverPropTextRight",
							'OnLayoutComplete', function (self)
								self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
								self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
							end,
							'Text', T(724608997137, --[[ModItemXTemplate RolloverInventoryWeaponBase Text]] "Уровень защиты"),
						}, {
							PlaceObj('XTemplateFunc', {
								'name', "Open(self,...)",
								'func', function (self,...)
									self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
									self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
									XWindow.Open(self,...)
									self.idPropVal:SetValueText("")
									self.idPropVal:SetNameText(T(890000000001415, "Возможность установки плиты"))
								end,
							}),
							}),"""

old_face = """						PlaceObj('XTemplateTemplate', {
							'comment', "Canholdplate",
							'__condition', function (parent, context) local cnt = ResolvePropObj(context); return  IsKindOf(cnt, "Armor") and (cnt.Slot == "Head" or not  cnt.Slot) and cnt.BlockFaceSlot end,
							'__template', "RolloverPropTextRight",
							'OnLayoutComplete', function (self)
								self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
								self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
							end,
							'BindTo', "CanHoldPlate",
							'Text', T(516469303127, --[[ModItemXTemplate RolloverInventoryWeaponBase Text]] "Уровень защиты"),
							'PercentValue', true,
						}, {
							PlaceObj('XTemplateFunc', {
								'name', "Open(self,...)",
								'func', function (self,...)
									self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
									self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
									XPropControl.Open(self,...)
									
									
									local cnt = ResolvePropObj(self.context);
									
									
									self.idPropVal:SetNameText(T(890000000001414, "Блокирует слот лица"))
									self.idPropVal:SetValueText("")
								end,
							}),
							}),"""

new_face = """						PlaceObj('XTemplateTemplate', {
							'comment', "Canholdplate",
							'__condition', function (parent, context) local cnt = ResolvePropObj(context); return  IsKindOf(cnt, "Armor") and (cnt.Slot == "Head" or not  cnt.Slot) and cnt.BlockFaceSlot end,
							'__template', "RolloverPropTextRight",
							'OnLayoutComplete', function (self)
								self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
								self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
							end,
							'Text', T(516469303127, --[[ModItemXTemplate RolloverInventoryWeaponBase Text]] "Уровень защиты"),
						}, {
							PlaceObj('XTemplateFunc', {
								'name', "Open(self,...)",
								'func', function (self,...)
									self.idPropVal:SetTextStyle("PDABrowserFlavorMedium")
									self.idPropVal:SetTextStyleRight("PDAActivityDescriptionWounds")
									XWindow.Open(self,...)
									self.idPropVal:SetNameText(T(890000000001414, "Блокирует слот лица"))
									self.idPropVal:SetValueText("")
								end,
							}),
							}),"""

nl = "\r\n" if "\r\n" in orig else "\n"
old_plate = old_plate.replace("\n", nl)
new_plate = new_plate.replace("\n", nl)
old_face = old_face.replace("\n", nl)
new_face = new_face.replace("\n", nl)

if old_plate not in text:
	raise SystemExit("CanHoldPlate block not found")
if old_face not in text:
	raise SystemExit("BlockFaceSlot block not found")
text = text.replace(old_plate, new_plate, 1)
text = text.replace(old_face, new_face, 1)

if text == orig and removed == 0:
	raise SystemExit("no changes")
path.write_bytes(text.encode("utf-8"))
print(f"removed nested idContainer Ids: {removed}")
print("patched CanHoldPlate/BlockFaceSlot rollover binds")
