# iab207-assignment2-evnt-mngmt-app-Gr53

IAB207 Assignmetn 2 web app: repo for full deployemnt of event management web app

In VS code open a folder you want this to go into
then open powershell terminal in VS code
Run the commands under the number sections

1. Clone:
   git clone https://github.com/AKeldrskrll/iab207-assignment2-evnt-mngmt-app-Gr53.git
   cd iab207-assignment2-evnt-mngmt-app-Gr53

2. Create & activate venv:
   python -m venv venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1

3. Install dependencies:
   pip install -r requirements.txt

4. Run the app:
   python main.py
   The app should be at http://127.0.0.1:5000/
