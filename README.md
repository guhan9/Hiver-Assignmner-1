# Hiver-Assignmner-1 : Assignment on mail
## Problem Statement
We have a 4 member team and we use gmail for our team. We all get emails and we want to share emails without having to forward them amongst one another. This needs to be done automatically, and we don't want any duplicate copies of the emails. We only want to share emails which have the subject - "Training Exercise". We also want to easily identify such shared emails with a label so that we can view them in Gmail by searching for the label.

Note: the assignment will be mainly judged on how you both work as a team. Negative points to both if any one doesn't meet the expected result. Chill, you can ping me or @Vani Gupta anytime.

Basic Use Cases

  1.An email E1 is sent to user A (Mandatory)

    Expected Results:

      Users B,C,D have a single copy of the same email (note :- email should not be resent/forwarded)

      Users A,B,C,D all have a label called "Training Exercise" for the email E1

  2.An email E2 is sent as a reply to E1 from any user (let's say B Optional)

    Expected Results:

      Users A,C,D have copy of email E2 and it should be in the same thread as E1 for these users

      Email E2 as well has the label "Training Exercise"

  3.A new email E3 is sent to two users (let's say A and B)

    Expected Results:

      Users A and B should not get any duplicate copy of E3

      Users C and D have the copy of E3

      All users have label "Training Exercise" applied on email E3

Tasks
    All these require use of gmail apis, which need OAuth tokens. We must store and refresh OAuth Tokens periodically. Write a background script which does that periodically. 

    Automatically detect new emails using Gmail pub/sub and call the logic that shares (or decides not to share) these emails to the users that do not have them 

Write the sharing logic which also applies the training exercise label making use of gmail apis. 
the above will be a group project, let's discuss on how you both shall split the tasks and work as a team.

Nuclino link - https://app.nuclino.com/Hiver/Hiver-Engineering/Training-Assignment---Interns-5ae1e6ab-4b5e-4481-8530-811cb2731123

Note: These are documentation links needed for working on the above problem statement. 

Gmail APIs : Gmail API | Google Developers

Google OAuth Playground : OAuth 2.0 Playground (Useful for doing POCs on google apis)

Google Pub/Sub : Method: projects.subscriptions.pull | Cloud Pub/Sub Documentation | Google Cloud (Pull method of listening to gmail pub sub)

Google OAuth : Using OAuth 2.0 for Web Server Applications | Google... 



Have fun exploring gmail apis guys!
