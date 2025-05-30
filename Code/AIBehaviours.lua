function AIBehavior:OnStart(unit)

    if (self.VoiceResponse or "") ~= "" then
		PlayVoiceResponse(unit, self.VoiceResponse)
	end
    
	self:OnActivate(unit)
end
