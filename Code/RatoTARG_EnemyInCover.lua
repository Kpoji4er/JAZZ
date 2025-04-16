DefineClass.AITargetingEnemyInCover = {
    __parents = {"AITargetingPolicy"},
    __generated_by_class = "ClassDef",
    properties = {{id = "Score", editor = "number", default = 100}}
}

function AITargetingEnemyInCover:EvalTarget(unit, target)

    local target_cover = GetCoverFrom(GetPackedPosAndStance(target), GetPackedPosAndStance(unit))

    -- local target_id = target.session_id
    -- ic(target_id, target_cover, target_cover == const.CoverLow or target_cover == const.CoverHigh)

    if target_cover == const.CoverLow or target_cover == const.CoverHigh then
        return self.Score or 100
    end
    return 0
end
