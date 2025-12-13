# RufusAI
This project experiments using a Large Lanaguage Model (LLM) as a tech support assistant.

The application will attempt to leverage Google Gemini Live API to handle calls and respond with solutions or steps to the user's issue, including support that may be specific to Ohio University procedure/policies.

This proposed system should reduce wait times and improve user satisfaction.


## Documentation
- [Project Presentation](https://catmailohio-my.sharepoint.com/:p:/g/personal/mb246721_ohio_edu/EUjtuziAv7RHop4Zsk_ypGoBhwmF36g_3umXW83kjWg4Pw?e=vgBKCZ)
- [Research Paper](https://www.overleaf.com/read/zgybhzcrbzmb#abdaf0)

## Current Acceptance Criteria (Subject to Change)
- The script uses the Gemini API to generate responses.
- It gets the API key from an environment variable.
- The script handles the case where the API key is not set.
- It generates three different responses based on user queries about Ohio University IT support.
- The responses are printed to the console.
- Accuracy is ≥ 50%

## RufusAI Setup
- Clone the repository with `git clone https://github.com/mbernay/rufusbot.git`, or by downloading the ZIP file and extracting it.
- Install dependencies by utilizing the [Makefile](https://github.com/mbernay/rufusbot/blob/0ae448fb3a1f8a010eaae28ac0fad596adfb7076/Makefile) using `make install-dependencies` or with `pip install -r requirements.txt`
- Run using `make run` or with `python rufusai.py`

## API Key Setup
In Powershell:
```
$env:GEMINI_API_KEY="yourapikey"
```
