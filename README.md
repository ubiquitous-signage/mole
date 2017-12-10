# mole
DUCRB API crawler for ubiquitous-signage

## Run
```
export DUCRB_API_USERNAME="username"
export DUCRB_API_PASSWORD="password"
python main.py
```
### (Optional) enable exit notification to Slack
```
export SLACK_INCOMING_WEBHOOK_URL="webhook url"
python main.py --slack
```