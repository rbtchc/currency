#!/bin/bash

appcfg.py update app.yaml
appcfg.py update_cron $PWD
appcfg.py update_indexes $PWD
