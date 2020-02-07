from string import Template
# import the smtplib module. It should be included in Python by default
import smtplib, ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for line in contacts_file:
            splitline = line.split(',')
            name = splitline[0]
            email = splitline[1]
            names.append(name)
            emails.append(email)
    return (names, emails)

def get_html(filename):
    with open(filename, 'r') as html_file:
        html = html_file.read()
    return html


def main():

    # set up the SMTP server
    MY_ADDRESS = sys.argv[1]
    password = sys.argv[2]
    homework_id = sys.argv[3]
    contacts_filename = "contacts.txt" #sys.argv[3]
    message_filename = "message.txt" #sys.argv[4]

    try:
        # Set the default socket timeout to a value that prevents connections
        # to our SMTP server from timing out, due to sendmail's greeting pause
        # feature.
        #socket.setdefaulttimeout(100)

        port = 465
        context = ssl.create_default_context()
        s = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        #s.ehlo()

        #s.starttls()
        #s.ehlo

        s.login(MY_ADDRESS, password)

        names, emails = get_contacts(contacts_filename)  # read contacts
        message_template = read_template(message_filename)

        names, emails = get_contacts(contacts_filename)  # read contacts
        message_template = read_template(message_filename)
        not_submitted_list = []


        # For each contact, send the email:
        for name, email in zip(names, emails):
            msg = MIMEMultipart()       # create a message
            first_name = email.replace("@sjsu.edu", "").split(".")[0]
            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=first_name.title(), HOMEWORK = homework_id)

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email
            msg['Subject']=f"Graded sheets for {homework_id}"

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            graded_file_path = os.path.join(homework_id, name)
            if not os.path.exists(graded_file_path):
                not_submitted_list.append(name)
                continue

            graded_filenames = [f for f in os.listdir(graded_file_path) if f.endswith("html")]
            for graded_filename in graded_filenames:
                html = get_html(os.path.join(graded_file_path, graded_filename))
                html_attachment = MIMEText(html, 'html')
                html_attachment.add_header('Content-Disposition', 'attachment', filename=graded_filename)
                msg.attach(html_attachment)
            # send the message via the server set up earlier.
            s.send_message(msg)

            del msg
            print(f"Mail sent to {name}")
        # Send a message to self listing who hasn't submitted their HW
        if not_submitted_list:
            msg = MIMEMultipart()
            message = f"""The following people haven't submitted their homework"""
            for not_submitted in not_submitted_list:
                message += "\n" + not_submitted
            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=MY_ADDRESS
            msg['Subject']=f"Students who haven't submiited {homework_id}"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            # send the message via the server set up earlier.
            s.send_message(msg)
            # Terminate the SMTP session and close the connection
        s.quit()
    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    main()
