-- JAZZ-QOL-001: auto fast-forward for unseen AI units + free camera on non-player turns
-- Ally (Rebel) exception 2026-08-05: PoV almost always sees allies → unseen Fast never fired on
-- their turn; M1 Rebel AITurn felt slow even after PERF dest caps.

local function JAZZ_AutoFastForwardMode()
	return CurrentModOptions and CurrentModOptions.AutoFastForward or "Off"
end

local function JAZZ_IsUnseenByPoV(unit)
	if not IsValid(unit) or unit:IsDead() then
		return true
	end
	local pov = GetPoVTeam()
	if not pov then
		return true
	end
	return not HasVisibilityTo(pov, unit)
end

local function JAZZ_IsPlayerAllyAIUnit(unit)
	if not IsValid(unit) then
		return false
	end
	local team = unit.team
	if not team then
		return false
	end
	if team.side == "ally" then
		return true
	end
	return not not team.player_ally
end

--- Apply AutoFastForward for an AI unit.
--- phase: "behavior" (before behavior:Play) | "attacks" (before AIPlayAttacks; Always only)
function JAZZ_UpdateAutoFastForward(unit, phase)
	local mode = JAZZ_AutoFastForwardMode()
	if mode == "Off" then
		return
	end
	if not g_Combat or g_Combat.is_player_control then
		return
	end
	if phase == "attacks" and mode ~= "Always" then
		return
	end

	-- Allies (Rebels): always Fast when FF enabled — they are usually PoV-visible.
	-- Enemies: Fast only when unseen (Running/Always).
	local want = (JAZZ_IsPlayerAllyAIUnit(unit) or JAZZ_IsUnseenByPoV(unit)) and "Fast" or "Normal"
	if g_FastForwardGameSpeed == want then
		return
	end
	g_FastForwardGameSpeed = want
	UpdateFastForwardGameSpeed()
	ObjModified(Selection)
end

local function JAZZ_EnemyTurnFreeCameraEnabled()
	local opts = CurrentModOptions
	if not opts or opts.EnemyTurnFreeCamera == nil then
		return true
	end
	return not not opts.EnemyTurnFreeCamera
end

local function JAZZ_ShouldSkipCameraMoveLock()
	if not JAZZ_EnemyTurnFreeCameraEnabled() then
		return false
	end
	if g_AIExecutionController then
		return true
	end
	return g_Combat and not g_Combat.is_player_control
end

local JAZZ_OrigLockCameraMovement = LockCameraMovement
function LockCameraMovement(reason)
	if JAZZ_ShouldSkipCameraMoveLock() then
		return
	end
	return JAZZ_OrigLockCameraMovement(reason)
end

function OnMsg.ExecutionControllerActivate()
	if not JAZZ_EnemyTurnFreeCameraEnabled() then
		return
	end
	UnlockCameraMovement(false, "unlock_all")
end
