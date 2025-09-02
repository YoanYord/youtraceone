## 🕵️ YouTraceOne - Simple OSINT Tool                                                 
**YouTraceOne** is a tool for quickly investigating **phone numbers** and **usernames** across popular platforms. It’s lightweight, terminal-friendly, and easy to extend.  

## ✨ Features
- **Phone Number Lookup**
  - Validate phone numbers  
  - Extract region codes, carriers, and timezones  
  - Auto-generate Google Dorks  

- **Username Enumeration**
  - Check usernames across platforms (Instagram, GitHub, Reddit, Facebook, LinkedIn, YouTube, Pinterest)   
  - Returns direct profile links when found  

## 📦 Installation
```bash
git clone https://github.com/YoanYord/youtraceone.git
cd youtraceone
python3 -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## 🚀 Usage
Run the script from the command line using Python. It accepts two optional arguments:

<b>--phone {phone_number}:</b> Perform OSINT on the phone number - [include country code](https://www.countrycode.org/).<br>
<b>--username {username}:</b> Search for the given username across supported platforms.
<br>
<br>
<img width="621" height="338" alt="image" src="https://github.com/user-attachments/assets/bf28a294-00c6-4095-bd1b-7bf56a0194c3" />
<br>
<i>If no arguments are provided, the script will display the help menu. </i>
```
python3 youtraceone.py --phone +{phonenumber}
python3 youtraceone.py --username {username}
```

You can use one or both arguments in a single run.
```
python3 youtraceone.py --username exampleuser --phone +1234567890
```
This will run both searches sequentially.
## Contributing

Feel free to fork the repository and submit pull requests for new platforms, features, or bug fixes.
