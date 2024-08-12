# Uniqlo Scraper
Scrapes UNIQLO for price &amp; stock status for a given Product ID

# How To 
 1. Configure 'sender_email_creds.py'. YouTube link inside, this will be the email address that SENDS notifications.
 2. Add a receiver email* by running 'app.py', you will be prompted to enter an email address.
    - Receiver email can be manually changed in the 'target_email.txt' file
 3. Head over to 'http://127.0.0.1:5000/' where you can enter the 'product ID' (ex: E466334-000).
 4. Once entered you'll be redirected to a tables page where you can select whichever color / size combination*, click on 'Add Selected' to begin tracking.
    - Anything that is completely out of stock will not appear
 5. At the homepage you'll see all tracked products along with the size and color that have been added.
 6. By clicking 'Update All' if a change in the price or stock is detected a notification email will be sent to the email entered in step 2.
 7. Avoid spamming 'Update All' button.
 8. Shutdown the webpage with (CTRL + C) in the command line.

