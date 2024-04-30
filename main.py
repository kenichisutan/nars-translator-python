'''
             task ::= [budget] sentence                       (* task to be processed *)

         sentence ::= statement"." [tense] [truth]            (* judgement to be absorbed into beliefs *)
                    | statement"?" [tense]                    (* question on truth-value to be answered *)
                    | statement"!" [desire]                   (* goal to be realized by operations *)
                    | statement"@"                            (* question on desire-value to be answered *)

        statement ::= <"<">term copula term<">">              (* two terms related to each other *)
                    | <"(">term copula term<")">              (* two terms related to each other, new notation *)
                    | term                                    (* a term can name a statement *)
                    | "(^"word {","term} ")"                  (* an operation to be executed *)
                    | word"("term {","term} ")"               (* an operation to be executed, new notation *)

           copula ::= "-->"                                   (* inheritance *)
                    | "<->"                                   (* similarity *)
                    | "{--"                                   (* instance *)
                    | "--]"                                   (* property *)
                    | "{-]"                                   (* instance-property *)
                    | "==>"                                   (* implication *)
                    | "=/>"                                   (* predictive implication *)
                    | "=|>"                                   (* concurrent implication *)
                    | "=\>"                                  (* =\> retrospective implication *)
                    | "<=>"                                   (* equivalence *)
                    | "</>"                                   (* predictive equivalence *)
                    | "<|>"                                   (* concurrent equivalence *)

             term ::= word                                    (* an atomic constant term *)
                    | variable                                (* an atomic variable term *)
                    | compound-term                           (* a term with internal structure *)
                    | statement                               (* a statement can serve as a term *)

    compound-term ::= op-ext-set term {"," term} "}"          (* extensional set *)
                    | op-int-set term {"," term} "]"          (* intensional set *)
                    | "("op-multi"," term {"," term} ")"      (* with prefix operator *)
                    | "("op-single"," term "," term ")"       (* with prefix operator *)
                    | "(" term {op-multi term} ")"            (* with infix operator *)
                    | "(" term op-single term ")"             (* with infix operator *)
                    | "(" term {","term} ")"                  (* product, new notation *)
                    | "(" op-ext-image "," term {"," term} ")"(* special case, extensional image *)
                    | "(" op-int-image "," term {"," term} ")"(* special case, \ intensional image *)
                    | "(" op-negation "," term ")"            (* negation *)
                    | op-negation term                        (* negation, new notation *)

        op-int-set::= "["                                     (* intensional set *)
        op-ext-set::= "{"                                     (* extensional set *)
       op-negation::= "--"                                    (* negation *)
      op-int-image::= "\"                                    (* \ intensional image *)
      op-ext-image::= "/"                                     (* extensional image *)
         op-multi ::= "&&"                                    (* conjunction *)
                    | "*"                                     (* product *)
                    | "||"                                    (* disjunction *)
                    | "&|"                                    (* parallel events *)
                    | "&/"                                    (* sequential events *)
                    | "|"                                     (* intensional intersection *)
                    | "&"                                     (* extensional intersection *)
        op-single ::= "-"                                     (* extensional difference *)
                    | "~"                                     (* intensional difference *)

         variable ::= "$"word                                 (* independent variable *)
                    | "#"word                                 (* dependent variable *)
                    | "?"word                                 (* query variable in question *)

            tense ::= ":/:"                                   (* future event *)
                    | ":|:"                                   (* present event *)
                    | ":\:"                                   (* past event *)

           desire ::= truth                                   (* same format, different interpretations *)
            truth ::= <"%">frequency[<";">confidence]<"%">    (* two numbers in [0,1]x(0,1) *)
           budget ::= <"$">priority[<";">durability][<";">quality]<"$"> (* three numbers in [0,1]x(0,1)x[0,1] *)

               word : #"[^\ ]+"                               (* unicode string *)
           priority : #"([0]?\.[0-9]+|1\.[0]*|1|0)"           (* 0 <= x <= 1 *)
         durability : #"[0]?\.[0]*[1-9]{1}[0-9]*"             (* 0 <  x <  1 *)
            quality : #"([0]?\.[0-9]+|1\.[0]*|1|0)"           (* 0 <= x <= 1 *)
          frequency : #"([0]?\.[0-9]+|1\.[0]*|1|0)"           (* 0 <= x <= 1 *)
         confidence : #"[0]?\.[0]*[1-9]{1}[0-9]*"             (* 0 <  x <  1 *)
'''


def main():
    example1 = "<human --> lifeform>."
    example1_result = translate(example1)

    example2 = "<{tim} --> (/,livingIn,_,{graz})>."
    example2_result = translate(example2)

    example3 = "<sunglasses --> (&,[black],glasses)>."
    example3_result = translate(example3)

    example4 = "<{?who} --> murder>?"
    example4_result = translate(example4)

    example5 = "<{tim} --> (/,livingIn,_,{graz})>. %0%"
    example5_result = translate(example5)

    example6 = "<{tim} --> (/,livingIn,_,{graz})>. %50%"
    example6_result = translate(example6)

    example7 = "<$1 --> [aggressive]>."
    example7_result = translate(example7)

    print()
    print(example1)
    print("Result:", example1_result)

    print(example2)
    print("Result:", example2_result)

    print(example3)
    print("Result:", example3_result)

    print(example4)
    print("Result:", example4_result)

    print(example5)
    print("Result:", example5_result)

    print(example6)
    print("Result:", example6_result)

    print(example7)
    print("Result:", example7_result)


def translate(task):
    # Check if task includes a percentage at end
    probability = -1
    if task[-1:len(task)] == "%":
        tasks = task.split("%")
        task = tasks[0]
        task = task[0:-1]
        probability = int(tasks[1])
    print(probability)

    sentenceType = getSentenceType(task)
    if sentenceType == -1:
        print("Invalid sentence type")
        return

    # Remove < and >
    task = task[ 1:-2 ]

    # Split task by space
    task = task.split(" ")
    print("Task:", task)

    # Get copula
    copula = getCopula(task[ 1 ])
    if copula == -1:
        print("Invalid copula")
        return

    # Get compound term for first term
    term1_type = getCompoundTerm(task[ 0 ])

    # Check if second term contains a verb
    term2_check = task[ 2 ].split(",")

    # Create a new list to store the filtered entries
    filtered_term2_check = [ ]

    # Iterate over each entry in term2_check
    for entry in term2_check:
        # Check if the entry contains alphanumeric characters
        if any(char.isalnum() for char in entry):
            # If it does, add it to the filtered list
            filtered_term2_check.append(entry)

    # Update term2_check with the filtered list
    term2_check = filtered_term2_check
    print("Term2 check:", term2_check)
    verb = ""
    term2_temp = ""
    if len(term2_check) > 1:
        verb = term2_check[ 0 ]
        term2_temp = term2_check[ 1 ]
    else:
        term2_temp = task[ 2 ]

    # Clean the verb of non alphanumeric characters
    for letter in verb:
        if not letter.isalnum():
            verb = verb.replace(letter, "")

    print("Verb:", verb)

    # Get compound term for second term
    term2_type = getCompoundTerm(term2_temp)

    # Remove non alphanumeric characters from terms
    term1 = ""
    for letter in task[ 0 ]:
        if letter.isalnum():
            term1 += letter

    if term1_type == 2:
        term1 = "someone that"

    term2 = ""
    for letter in term2_temp:
        if letter.isalnum():
            term2 += letter

    # Construct sentence
    result = constructSentence(sentenceType, copula, term1, term2, term1_type, term2_type, verb, probability)

    return result


def getSentenceType(sentence):
    print("Sentence:", sentence)
    # determine type of sentence
    match sentence[ -1 ]:
        case ".":
            return 1
        case "?":
            return 2
        case "!":
            return 3
        case "@":
            return 4
        case _:
            return -1


def getCopula(copula):
    print("Copula:", copula)
    # determine copula
    match copula:
        case "-->":
            return 1
        case "<->":
            return 2
        case "{--":
            return 3
        case "--]":
            return 4
        case "{-]":
            return 5
        case "==>":
            return 6
        case "=/>":
            return 7
        case "=|>":
            return 8
        case "=\>":
            return 9
        case "<=>":
            return 10
        case "</>":
            return 11
        case "<|>":
            return 12
        case _:
            return -1


def getCompoundTerm(term):
    # Remove letters from term
    for letter in term:
        if letter.isalpha():
            term = term.replace(letter, "")

    # determine term
    term = term[0:1]
    print("Term:", term)
    match term:
        case "{":
            return 1
        case "$":
            return 2
        case _:
            return -1


def constructSentence(sentenceType, copulaType, term1, term2, term1_type, term2_type, verb, probability):
    print("Constructing sentence")
    # Construct sentence
    result = ""

    copula_str = ""

    if verb != "":
        verb = " " + verb

    # Check if verb has a capital letter
    for letter in verb:
        if letter.isupper():
            verb = verb.replace(letter, " " + letter.lower())

    match copulaType:
        case 1:
            copula_str = "is"
            if term1_type == -1:
                if term1[ -1 ] != "s":
                    term1 += "s"
                if term2[ -1 ] != "s":
                    term2 += "s"
                copula_str = "are"
            elif verb == "":
                verb = " (the)"

    match sentenceType:
        case 1:
            result = term1 + " " + copula_str + verb + " " + term2
        case 2:
            result = term1 + " " + copula_str + verb + " " + term2 + "?"

    match probability:
        case 0:
            result = term1 + " " + copula_str + " not" + verb + " " + term2
        case -1:
            pass
        case _:
            result = "There is a " + str(probability) + "% chance that " + result

    # Capitalize first letter
    result = result[0].upper() + result[1:]

    return result


if __name__ == "__main__":
    main()
