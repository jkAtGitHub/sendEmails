from string import Template
# import the smtplib module. It should be included in Python by default
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    contacts_filename = sys.argv[3]
    message_filename = sys.argv[4]

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, password)

    names, emails = get_contacts(contacts_filename)  # read contacts
    message_template = read_template(message_filename)



    # For each contact, send the email:
    for name, email in zip(names, emails):
        print(f"Sending mail to {name}")
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is not a DRILL; Houston Calling"


        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        filename = "data/_frdkl_sine.html"
        html = get_html(filename)
        part2 = MIMEText(html, 'html')
        part2.add_header('Content-Disposition', 'attachment', filename=filename)

        msg.attach(part2)

        # send the message via the server set up earlier.
        s.send_message(msg)

        del msg
        # Terminate the SMTP session and close the connection
    s.quit()



if __name__ == '__main__':
    main()
