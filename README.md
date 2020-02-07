# Send Auto Emails
## Send graded results to contact list

STEP0. Goto https://myaccount.google.com/lesssecureapps ; signin to the gmail account from which emails will be sent and turn the Allow less secure apps switch to **ON**

**STEP1.** Save the `contacts.txt` file in the following format:
    - name,emailid

**STEP2.** Modify the `message.txt` to edit the template.

**STEP3.** Place the homework folder in the same folder as the script. The homework folder structure should be
  - <homework_folder_name>
    - student_name (should match the name in the contacts.txt)
      - graded_file1.html
      - graded_file2.html

**STEP4.** Execute the Python script <br/>
```python sendEmails.py <sender_emailid> <sender_email_password> <homework_folder_name>```
