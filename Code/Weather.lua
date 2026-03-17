WeatherCycle = {
	Wet = {
		{ "ClearSky",  100, 6, 36 },
		{ "RainLight", 50, 3, 18 },
		{ "RainHeavy",  30, 3, 12 },
		{ "Fog",        60, 1, 9 },
	},
	Dry = {
		{ "ClearSky",  100, 8, 24 },
		{ "Heat",       60, 4, 10 },
		{ "DustStorm",  35, 2, 8 },
		{ "FireStorm",  10, 1, 4 },
	},
	CursedForest = {		
		{ "RainLight", 100, 12, 36 },
		{ "Fog",        50, 12, 24 },
	},
}

function CalculateWeatherForSector(weather_cycle, weather_zone, time)
    local hours = time / const.Scale.h
    local cycle = GetCurrentWeatherCycle()[weather_cycle]
    local wrand = BraidRandomCreate(Game.id, weather_zone)
    local h = 0
    local hours_in_day = const.Scale.day / const.Scale.h

    while true do
        for i, w in ipairs(cycle) do
            --print("weather check")
            local weather = w[1]
            local start_hour_in_day = h % hours_in_day
            local allowed = true

            if weather == "Fog" then
                allowed = start_hour_in_day >= 3 and start_hour_in_day < 6
            elseif weather == "Heat" then
                allowed = start_hour_in_day >= 10 and start_hour_in_day < 18
            elseif weather == "FireStorm" then
                allowed = start_hour_in_day >= 10 and start_hour_in_day < 18
            end

            if allowed and wrand(100) < w[2] then
                h = h + wrand(w[3], w[4])
                if hours < h then
                   -- print(weather)
                    return weather
                end
            end
        end
    end
end