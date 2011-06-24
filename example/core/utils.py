import sys
from random import Random

def generate_password(passwordLength=8, alternate_hands=True):
    """Generate a random password of passwordLength length and possibly with
    alternating characters for left/right hand
    """
    rng = Random()
    
    righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
    lefthand = '789yuiophjknmYUIPHJKLNM'
    allchars = righthand + lefthand
    
    password = ""
    for i in range(passwordLength):
        if not alternate_hands:
            password += rng.choice(allchars)
        else:
            if i%2:
                password += rng.choice(lefthand)
            else:
                password += rng.choice(righthand)

    return password

