UndefineClass('HealWounds')
DefineClass.HealWounds = {
	__parents = { "Effect", },
	__generated_by_class = "EffectDef",

	RequiredObjClasses = {
	"Unit",
},
	EditorView = Untranslated("Heal unit's wounds"),
	Documentation = "Heals unit's wounds",
	EditorNestedObjCategory = "Units",
}

function HealWounds:__exec(obj, context)
	obj:RemoveStatusEffect("Wounded", "all")
	obj:RemoveStatusEffect("Inaccurate", "all")
	obj:RemoveStatusEffect("Slowed", "all")
	obj:RemoveStatusEffect("Bleeding", "all")
end

PlaceObj('EffectDef', {
	group = "Effects",
	id = "HealWounds",
	PlaceObj('ClassConstDef', {
		'name', "RequiredObjClasses",
		'type', "string_list",
		'value', {
			"Unit",
		},
	}),
	PlaceObj('ClassConstDef', {
		'name', "EditorView",
		'type', "text",
		'value', "Heal unit's wounds",
		'untranslated', true,
	}),
	PlaceObj('ClassConstDef', {
		'name', "Documentation",
		'type', "text",
		'value', "Heals unit's wounds",
	}),
	PlaceObj('ClassMethodDef', {
		'name', "__exec",
		'params', "obj, context",
		'code', function (self, obj, context)
			obj:RemoveStatusEffect("Wounded", "all")
			obj:RemoveStatusEffect("Inaccurate", "all")
			obj:RemoveStatusEffect("Slowed", "all")
			obj:RemoveStatusEffect("Bleeding", "all")		
		end,
	}),
	PlaceObj('ClassConstDef', {
		'name', "EditorNestedObjCategory",
		'type', "text",
		'value', "Units",
	}),
	PlaceObj('TestHarness', {
		'name', "TestHarness",
		'TestedOnce', true,
		'Tested', true,
		'GetTestSubject', function (self) return SelectedObj end,
		'TestObject', PlaceObj('HealWounds', {}),
	}),
})

