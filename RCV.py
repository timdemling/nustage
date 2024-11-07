import csv
import os

# INPUT YOUR CSV FILEPATH HERE
csv_filepath = "C:\\Users\\timde\\Downloads\\Spring 2024 Mainstage Second and Third Choice.csv"

def get_ballots_from_csv(csv_filepath):

    # this ensures that the filepath matches the operating system syntax
    universal_filepath = os.path.join(csv_filepath)

    # Open the CSV file and read its contents into a list of lists
    with open(universal_filepath) as f:
        
        # create csv reader object
        reader = csv.reader(f)

        # read each line of the csv into "original_votes" list
        # first column of the csv is presumed to be submission datetime - row[1:] filters this out
        # original_votes will be of the form [[choice1, choice2, choice3, choice4, choice5], [choice1, choice2, ...], ...]
        original_votes = [row[1:] for row in reader]

    # initailize new list to hold valid ballots
    clean_votes = []

    # for each ballot in the csv
    for ballot in original_votes:

        # sometimes '' shows up as a show choice due to the csv format - if it does, this will remove it
        if '' in ballot:
            ballot.remove('')
        
        # make everything lowercase in case of formatting differences - just a failsafe
        ballot_lowercase = [show.lower() for show in ballot]

        # this checks whether or not a ballot has duplicates - each show should appear exactly once
        has_duplicates = len(ballot_lowercase) != len(set(ballot_lowercase))

        ## if there is a duplicate show in the ballot, it will break the algo and must be deleted
        # if there is not a duplicate
        if not has_duplicates:

            # add the lowercase ballot to the clean_votes
            clean_votes.append(ballot_lowercase)


    # the first row of the csv is the header row: [Submission time, choice1, choice2, ...]
    # remove it    
    clean_votes = clean_votes[1:]

    return clean_votes


# these are all of the helper functions that does everything. run it
def tally_first_place_votes(votes_list: list) -> dict:
    """
    Takes votes_list and tallys the first place votes for each show, and returns them as a dictionary

    Args:
        - votes_list (list): list of ballots of the form [[choice1, choice2, choice3, choice4, choice5], [], [], ... ]
    
    Returns:
        - first_place_votes (dict): keys of show name (str), values of first place vote totals (int)
        e.g. {'Shrek The Musical': 8, 'The Prom': 14, 'Chicago': 17, 'Catch Me If You Can': 10, 'Legally Blonde': 8}

    """

    # initialize dictionary to hold vote totals
    first_place_votes = {}
    
    # for each ballot
    for ballot in votes_list:

        # first position in the ballot represents their first choice
        first_choice = ballot[0]

        ## so that we don't need to know the list of remaining shows, we'll 
        ## automatically create keys from the shows still on the ballot

        # if we don't already have the show in the dict
        if first_choice not in first_place_votes.keys():

            # create a new entry to the dictionary with vote total 1
            first_place_votes[first_choice] = 1

        # if the show is already in the dict
        else:

            # add 1 to the vote total
            first_place_votes[first_choice] += 1

    return first_place_votes

def display_winner(running_votes_dict: dict) -> bool:
    """
    Once we have determined that a winner has been found, print it out
    
    Args: 
        - running_votes_dict (dict): keys of show name (str), 
            values of vote total (int)
    
    Prints:
        - prints winner

    Returns:
        - True (bool): this is to set the win condition to True
    """

    # find the winning show
    winner = max(running_votes_dict, key=running_votes_dict.get)
    
    # print out the winner
    print(f"The winner is {winner}!")

    return True

def redistribute_last_place_votes(
        running_votes: list, 
        last_place_show: str
    )  -> list:
    """
    Takes the running list of votes and removes the last place show from each ballot. 
    this moves every show behind the last place show up
    
    e.g.
    - last place show is "Beauty and the Beast"
    - ballot is: ['BatB', 'Shrek', 'Pippin', 'Anything Goes', 'The Prom']
    - this removes 'BatB' the ballot to: ['Shrek', 'Pippin', 'Anything Goes', 'The Prom']
    - the ballot's first choice vote has been changed to 'Shrek', since it is
        now in the first position in the list
    - thus, after removing the last place show from every ballot, the first position
        show will represent the redistributed first choice, and we can tally first
        place votes as usual

    Args:
        - running_votes (list): A list of ballots (list), with past eliminated shows having been removed
            e.g. [[show1, show2, show3, show4, show5], [show1, show2, show3, show4, show5], ... ]
        - last_place_show (str): the exact string of the show which has been eliminated

    Returns: 
        - new_votes (list): a list of ballots (list), with the last_place_show having been removed in 
            addition to those removed in the past
    """

    # set a list for new votes
    new_votes = []

    # for each ballot in the running votes
    for ballot in running_votes:

        # define a new empty ballot
        new_ballot = []

        # for each of their shows
        for choice in ballot:

            # if it isn't the last place show
            if choice != last_place_show:

                # add it to the new ballot
                new_ballot.append(choice)

        # once all the shows except the last place show have been added (in order)
        # add the ballot to the new list of votes
        new_votes.append(new_ballot)    
        
    return new_votes

def determine_winner(csv_filepath):
    """
    This is the main function that calls all secondary functions 
    and determines the winner from the list of votes

    Args:
        - votes_list (list): list of ballots of the form
            [[choice1, choice2, choice3, choice4, choice5], [choice1, choice2, ...], [...], ... ]

    Prints:
        - for each round, prints current vote tally, whether there's a winner, last place show, redistribution
        - once a winner has been found, prints out the winner!
    """
    
    # get votes_list from csv_filepath
    votes_list = get_ballots_from_csv(csv_filepath)
    
    # get the tally of first place votes from the votes list
    running_votes_dict = tally_first_place_votes(votes_list)
    running_votes = votes_list.copy()

    # print out the first place votes
    print("The first place vote totals are: ")
    print(running_votes_dict)
    print("\n")
    
    # determine the threshold votes value (50% + 1)
    threshold = len(votes_list) / 2

    # initialize the win condition to FALSE
    win = False

    # while we still don't have a winner
    while win == False:

        # find the highest vote count
        max_votes = max(running_votes_dict.values())

        # if that vote count exceeds 50% + 1, we have a winner!
        if max_votes > threshold:

            win = display_winner(running_votes_dict)

        # if no show exceeds 50% + 1
        else:

            # print that no show met the threshold
            print(f"No show's total exceeded the threshold of {threshold}")

            # find the show with the least number of first place votes
            last_place_show = min(running_votes_dict, key=running_votes_dict.get)

            # print out the eliminated show
            print(f"{last_place_show} came in last place and will be eliminated.")

            # remove last place show from every ballot
            new_votes = redistribute_last_place_votes(running_votes, last_place_show)

            # redefine running votes to this new list of votes
            running_votes = new_votes.copy()

            # from these new ballots, compute first place vote totals
            running_votes_dict = tally_first_place_votes(running_votes)

            # print out the running vote totals
            print(f"After redistributing {last_place_show}'s votes, the tally is:")
            print(running_votes_dict)
            print("\n")

determine_winner(csv_filepath)
