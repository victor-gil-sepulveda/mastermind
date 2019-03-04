
def get_feedback(code, guess):
    """
    This performs a naive check of a guess against a code an returns a feedback. A feedback string
    is composed of four chars in ['_', '1', '2']. For each character in the guess that coincides in
    color with one character in the code, the feedback will contain a '1'. For each character in the
    guess that coincides in color and position with one character in the code, the feedback will include
    a '2'. The feedback will be a blank ('_') otherwise.
    Each guess and code is formed of 7 different characters (from 1 to 6), one for each color,  and
    the 'blank' one ('_').
    Ex. code     = "23_4"
        guess    = "214_"
        feedback = "21__" -> a 2 because 2 <-> 2, a 1 because of the four, and two blanks.
    """
    feedback = ""
    code_l = list(code)
    for pos in range(len(guess)):
        c = guess[pos]
        try:
            pos_in_code = code_l.index(c)
            if pos == pos_in_code:
                c_fb = "2" # found and in the same pos
            else:
                c_fb = "1" # just found somewhere
            code_l[pos_in_code] = "X" # we do not want to compare with this one again
        except ValueError:
            c_fb = "_" # not found
        feedback += c_fb
    return feedback
