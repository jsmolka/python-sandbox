def yes_no(message):
    """Prints yes/no dialog"""
    message = message + " (y/n)"
    print(message)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Invalid answer! Try again!")


def enter(action):
    """Prints enter message"""
    input("Press enter to {0}...".format(action))


def __only_spaces_or_empty(string):
    """Checks if string only contains spaces"""
    if string == "":
        return True
    else:
        for char in string:
            if char != " ":
                return False
        return True


def user_input(*answers, create_range=False):
    """Processes user input"""
    if not answers:
        raise Exception("Answers cannot be empty")

    if create_range and len(answers) != 2:
        raise Exception("Create range is only defines for two values in the answer list")

    try:
        if len(answers) == 1 and type(answers[0]) == list:  # Extract list
            answers = answers[0]

        answers = list(answers)
        if create_range:
            if type(answers[0]) == int and type(answers[1]) == int:
                answers.sort()
                start = answers[0]
                end = answers[1]
                answers = []
                for i in range(start, end):
                    answers.append(i)

        answer_type = type(answers[0])

        while True:
            answer = input()
            while __only_spaces_or_empty(answer):
                print("Invalid answer! Try again!")
                answer = input()

            try:
                answer = answer_type(answer)
                if answer in answers:
                    return answer
                else:
                    print("Invalid answer! Try again!")
            except:
                print("Invalid answer! Try again!")

    except Exception as e:
        print("Something went wrong while processing the user input")
        print(str(e))
        if answers:
            print("Returned first value of answer list")
            return answers[0]
        else:
            print("Returned empty string")
            return ""
