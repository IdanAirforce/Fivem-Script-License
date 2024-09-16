CreateThread(function()
    Wait(100)
    local license = Config.License

    PerformHttpRequest("http://localhost:5000/check_license", function(err2, response, headers2)
        if err2 ~= 200 then
            print('[Airforce] Connection error')
            Wait(2500)
            os.exit()
        else
            local data = json.decode(response)
            if data.valid then
                print('[Airforce] Authorized.')
            else
                print('[Airforce] License is invalid.')
                Wait(2500)
                os.exit()
            end
        end
    end, 'POST', json.encode({ license_key = license }), { ['Content-Type'] = 'application/json' })
        
end)
