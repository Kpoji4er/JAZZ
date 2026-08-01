hr.CameraTacMaxZoom = 180
hr.CameraTacMinZoom = 30
hr.CameraTacMaxZoomOverview = 730

-- Vanilla gap after combat / Max setpieces:
-- AdjustCombatCamera("reset") restores hr.CameraTacLookAtAngle but does not call
-- cameraTac.SetLookAtAngle. Setpieces with RestoreCamera=false only run
-- SetupInitialCamera when cameraTac is inactive. Live pitch can stay at the
-- enemy-turn 40° (or Max cutscene leave-behind) until save/load, which calls
-- cameraTac.SetupLookAtAngle via LoadSessionData.

local function JAZZ_RestoreEnemyTurnCameraHr()
	if table.changed(hr, "Instant Vertical Camera Movement") then
		table.restore(hr, "Instant Vertical Camera Movement")
	end
	if table.changed(hr, "Enemy turn TacCamera Angle") then
		table.restore(hr, "Enemy turn TacCamera Angle")
	end
	if table.changed(hr, "Enemy turn TacCamera Height") then
		table.restore(hr, "Enemy turn TacCamera Height")
	end
end

function JAZZ_RestoreTacCameraControl()
	if IsSetpiecePlaying() then
		return
	end
	if IsMainMenuMap and IsMainMenuMap() then
		return
	end

	JAZZ_RestoreEnemyTurnCameraHr()
	hr.CameraTacClampToTerrain = true

	if cameraTac.GetForceMaxZoom and cameraTac.GetForceMaxZoom() then
		cameraTac.SetForceMaxZoom(false)
	end

	if UnlockCameraMovement then
		UnlockCameraMovement(false, "unlock_all")
	end
	if cameraTac.SetLockedMovement then
		cameraTac.SetLockedMovement(false)
	end

	if not cameraTac.IsActive() then
		cameraTac.Activate(true)
	end

	if cameraTac.SetupLookAtAngle then
		cameraTac.SetupLookAtAngle()
	else
		local overview = cameraTac.GetIsInOverview and cameraTac.GetIsInOverview()
		local angle = overview and hr.CameraTacLookAtAngleInOverview or hr.CameraTacLookAtAngle
		cameraTac.SetLookAtAngle(angle)
	end
end

function OnMsg.SetpieceDialogClosed()
	-- XSetpieceDlg keeps XCameraLockLayer until Close a few frames later.
	CreateRealTimeThread(function()
		for _ = 1, 12 do
			if not GetDialog("XSetpieceDlg") then
				break
			end
			WaitNextFrame(1)
		end
		JAZZ_RestoreTacCameraControl()
	end)
end

function OnMsg.CombatEnd()
	-- Same live-pitch gap after AdjustCombatCamera("reset") in Combat:End.
	CreateGameTimeThread(function()
		Sleep(1)
		if IsSetpiecePlaying() then
			return
		end
		JAZZ_RestoreTacCameraControl()
	end)
end
