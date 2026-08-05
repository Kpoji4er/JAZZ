-- Satellite region border overlay: ownership fill stays vanilla Side tint;
-- thick colored outlines follow each authored Region perimeter.
-- Rebuild edge cache when sat opens / layers change; draw after vanilla DrawContent.

g_JAZZ_SatRegionBordersWrapped = rawget(_G, "g_JAZZ_SatRegionBordersWrapped") or false
g_JAZZ_SatRegionBordersBase = rawget(_G, "g_JAZZ_SatRegionBordersBase") or false

local lEdgeCache = false
local lEdgeCacheKey = false
-- Outer stroke + inner stroke for readable sat-scale contours.
local lLineWidthOuter = 10
local lLineWidthInner = 6
local lInset = 3

local lPalette = {
	RGB(255, 196, 64),
	RGB(64, 196, 255),
	RGB(255, 96, 176),
	RGB(96, 230, 120),
	RGB(255, 140, 64),
	RGB(176, 120, 255),
	RGB(255, 72, 72),
	RGB(72, 230, 200),
	RGB(220, 220, 100),
	RGB(140, 180, 255),
}

local function lRegionId(region)
	if not region or region == "none" then
		return false
	end
	return region.id or region.Id or false
end

local function lColorForRegionId(rid)
	if not rid then
		return RGB(200, 200, 200)
	end
	local h = 0
	for i = 1, #rid do
		h = (h * 33 + string.byte(rid, i)) % 2147483647
	end
	return lPalette[1 + (h % #lPalette)]
end

local lUnderlayColor = RGB(20, 20, 20)

local function lBuildSectorRegionMap()
	local map = {}
	if not GetRegionForSector then
		return map
	end
	for sector_id, sector in pairs(gv_Sectors or empty_table) do
		if sector and sector.Id and not (IsSectorUnderground and IsSectorUnderground(sector.Id)) then
			local region = GetRegionForSector(sector.Id)
			local rid = lRegionId(region)
			if rid then
				map[sector.Id] = rid
			end
		end
	end
	return map
end

local function lCacheKey(sat)
	return string.format(
		"%s|%s|%s|%s|%s",
		tostring(Game and Game.Campaign or ""),
		tostring(sat and sat.layer_mode or ""),
		tostring(sat and sat.sector_max_x or 0),
		tostring(sat and sat.sector_max_y or 0),
		tostring(sat and sat.sector_size and sat.sector_size:x() or 0)
	)
end

local function lNeighborRegionId(region_of, sector_id, dir)
	local nid = GetNeighborSector and GetNeighborSector(sector_id, dir)
	if not nid then
		return false -- map edge = outside region
	end
	return region_of[nid] or false
end

--- Full perimeter of each region cell (neighbor missing or different Region Id).
--- Segments overlap at corners slightly so the stroke does not break.
local function lRebuildEdgeCache(sat)
	lEdgeCache = {}
	lEdgeCacheKey = lCacheKey(sat)
	if not sat or not sat.grid_start or not sat.sector_size then
		return
	end
	local start_x = sat.grid_start:x()
	local start_y = sat.grid_start:y()
	local sx = sat.sector_size:x()
	local sy = sat.sector_size:y()
	local region_of = lBuildSectorRegionMap()
	if not next(region_of) then
		return
	end

	-- Corner overlap so adjacent segments meet under thick stroke.
	local overlap = Max(lLineWidthOuter, 4)

	local function add_edge(x1, y1, x2, y2, color)
		lEdgeCache[#lEdgeCache + 1] = {
			point(x1, y1),
			point(x2, y2),
			color,
		}
	end

	for sector_id, rid in pairs(region_of) do
		local row, col = sector_unpack(sector_id)
		if not row or not col then
			goto continue
		end
		local left = start_x + (col - 1) * sx
		local top = start_y + (row - 1) * sy
		local right = left + sx
		local bottom = top + sy
		local inset = Min(lInset, DivRound(Min(sx, sy), 8))
		local color = lColorForRegionId(rid)

		-- North
		if lNeighborRegionId(region_of, sector_id, "North") ~= rid then
			local y = top + inset
			add_edge(left - overlap, y, right + overlap, y, color)
		end
		-- South
		if lNeighborRegionId(region_of, sector_id, "South") ~= rid then
			local y = bottom - inset
			add_edge(left - overlap, y, right + overlap, y, color)
		end
		-- West
		if lNeighborRegionId(region_of, sector_id, "West") ~= rid then
			local x = left + inset
			add_edge(x, top - overlap, x, bottom + overlap, color)
		end
		-- East
		if lNeighborRegionId(region_of, sector_id, "East") ~= rid then
			local x = right - inset
			add_edge(x, top - overlap, x, bottom + overlap, color)
		end
		::continue::
	end
end

local function lEnsureEdgeCache(sat)
	local key = lCacheKey(sat)
	if not lEdgeCache or lEdgeCacheKey ~= key then
		lRebuildEdgeCache(sat)
	end
end

function JAZZ_InvalidateSatelliteRegionBorders()
	lEdgeCache = false
	lEdgeCacheKey = false
end

local function lDrawRegionBorders(sat)
	if not sat or sat.window_state == "destroying" then
		return
	end
	if sat.layer_mode == "underground" then
		return
	end
	lEnsureEdgeCache(sat)
	if not lEdgeCache or #lEdgeCache == 0 then
		return
	end
	if not UIL or not UIL.DrawLineAntialised then
		return
	end
	-- Dark underlay then bright stroke — reads at sat zoom.
	for i = 1, #lEdgeCache do
		local e = lEdgeCache[i]
		UIL.DrawLineAntialised(lLineWidthOuter, e[1], e[2], lUnderlayColor)
	end
	for i = 1, #lEdgeCache do
		local e = lEdgeCache[i]
		UIL.DrawLineAntialised(lLineWidthInner, e[1], e[2], e[3])
	end
end

local function lInstallDrawContentWrap()
	if rawget(_G, "g_JAZZ_SatRegionBordersWrapped") then
		return
	end
	if not XSatelliteViewMap or type(XSatelliteViewMap.DrawContent) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_SatRegionBordersBase", XSatelliteViewMap.DrawContent)
	rawset(_G, "g_JAZZ_SatRegionBordersWrapped", true)
	function XSatelliteViewMap:DrawContent()
		g_JAZZ_SatRegionBordersBase(self)
		local ok, err = pcall(lDrawRegionBorders, self)
		if not ok and rawget(_G, "Platform") and Platform.developer then
			print("[JAZZ] region borders draw:", err)
		end
	end
end

function OnMsg.ClassesBuilt()
	lInstallDrawContentWrap()
end

function OnMsg.ModsReloaded()
	JAZZ_InvalidateSatelliteRegionBorders()
	lInstallDrawContentWrap()
end

function OnMsg.SatelliteViewOpened()
	JAZZ_InvalidateSatelliteRegionBorders()
end

function OnMsg.CampaignInitialized()
	JAZZ_InvalidateSatelliteRegionBorders()
end
