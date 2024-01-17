ClamScore = {data={}}

CLAMSCORE_REALM = string.gsub(GetRealmName(), ' ', '')

GameTooltip:HookScript("OnTooltipSetUnit", function(self)
    local unitName, unitId = self:GetUnit()
    if not UnitIsPlayer(unitId) then return end

    local parse = ClamScore['data'][CLAMSCORE_REALM][unitName][1]

	if parse == nil then return end

    local color = "|cff666666"
    if parse == '--' then
        color = "|cff666666"
    elseif parse < 25.0 then
        color = "|cff666666"
    elseif parse < 50.0 then
        color = "|cff1eff00"
    elseif parse < 75.0 then
        color = "|cff0070f3"
    elseif parse < 95.0 then
        color = "|cffa335ee"
    elseif parse < 99.0 then
        color = "|cffff8000"
    elseif parse < 100.0 then
        color = "|cffe268a8"
    else
        color = "|cffe5cc80"
    end

    self:AddLine("\nClamScore: " .. color .. parse .. "|r")
end)