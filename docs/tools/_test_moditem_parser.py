"""Regression coverage for the non-evaluating ModItem scanner."""
import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[2]/'.agents/skills/sync-jazz-generated-data/scripts/parse-moditems.py'
spec=importlib.util.spec_from_file_location('moditems',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ModItems(unittest.TestCase):
 def test_inline_entity(self):
  r=mod.records('PlaceObj(\'ModItemEntity\', { \'name\', "A", \'ClassParents\', {}, \'entity_name\', "A" })')
  self.assertEqual((r[0]['Name'],r[0]['EntityName']),('A','A'))
 def test_nested_and_comments(self):
  text='''-- PlaceObj('ModItemEntity', { 'entity_name', "fake" })
PlaceObj('ModItemFolder', { 'name', "Folder" }, {
 PlaceObj('ModItemUnitDataCompositeDef', {
       'Id', "Unit", 'Nested', { 'Id', "wrong" },
 'Description', "Don't read { braces } or PlaceObj here",
 }),
PlaceObj('ModItemWeaponComponent', { id = "C", data = function() return {} end }),
})'''
  r=mod.records(text)
  self.assertEqual([(x['Class'],x['Id']) for x in r],[('ModItemFolder',None),('ModItemUnitDataCompositeDef','Unit'),('ModItemWeaponComponent','C')])
 def test_long_strings(self):
  r=mod.records('''--[=[ fake } ]=]
PlaceObj('ModItemCode', { 'name', "module", 'Code', [==[ } 'id', "fake" ]==], 'CodeFileName', "Code/module.lua" })''')
  self.assertEqual(r[0]['CodeFileName'],'Code/module.lua')
 def test_broken_input(self):
  with self.assertRaises(ValueError):mod.records("PlaceObj('ModItemEntity', {")

if __name__=='__main__':unittest.main()
