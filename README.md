## NU Stage Ranked Choice Voting - Single Transferrable Vote - Algorithm

There really isn't a good website or existing program to easily do this process, so here we are. Written by Tim Demling '23

### Format of the google form (both absentee and in-person)
- Show names must be consistent across absentee/in-person voting
- The first question in the google form should be "choice 1", the second question should be "choice 2", etc.
- Questions should be multiple-choice selection so that all show names are the same
    - This is exactly the format of the google form used in the spring 2023 mainstage voting meeting

### Process of voting
- Have both absentee and in-person ballots in their own csv file (export from google sheets (results))
- Copy the votes from one onto the bottom of the other (or create a new file, it doesn't really matter, you just need one csv file with all votes)
- Copy the filepath of the csv file (e.g. `"C:\\Users\\timde\\Downloads\\Spring 2024 Mainstage Second and Third Choice.csv"`) and paste it next to `csv_filepath = `
    - NOTE: you may need to change the slashes in the filepath to double back-slashes. 


#### Order of votes
- Fall 1st choice
- Spring 1st choice
- Fall 2nd choice
- Spring 2nd/3rd choice

Note: For Spring 2nd/3rd choice, you'll need to run the algorithm twice. The first time, run it with all eligible shows for Spring backup. The second time, use the same ballots but remove the winner for backup from them and run the algorithm again. E.g. in Spring 2023 voting, Pippin was the winner for Spring, so every other show was on the ballot for backup. The winner for the backup was [I actually forget, say it's Shrek], so at the top of the algorithm there's a place to remove Shrek from the ballots. Then, the algorithm is run again without Shrek or Pippin to determine the winner of the 3rd place show. This is because the runner-up to the backup vote isn't necessarily the 3rd place choice since the people who voted for the show which came in 2nd (Shrek)'s votes need to be redistributed to their next choice in order to truly find the 3rd choice. 


- If someone selects a show for two different choices, their ballot will break the algorithm and so their vote will be deleted. Warn them of this