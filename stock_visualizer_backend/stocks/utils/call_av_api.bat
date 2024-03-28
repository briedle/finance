@echo off
echo [%date% %time%] Preventing the system from sleeping...
powercfg -change -standby-timeout-ac 0

echo [%date% %time%] Running the command...
bash -c "cd ~/web-projects/finance/stock_visualizer_backend && /home/briedle/.local/share/virtualenvs/finance-zPHMDCNI/bin/python manage.py sync_av_data time_series_weekly_adjusted --start-index 150 --stop-index 200"

echo [%date% %time%] Reverting power settings...
powercfg -change -standby-timeout-ac 30

echo [%date% %time%] Script completed.