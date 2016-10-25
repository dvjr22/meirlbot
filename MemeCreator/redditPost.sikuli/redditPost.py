debug = True

# Navigate to me_irl
click("1476808449106.png")
type("www.reddit.com/r/me_irl")
type(Key.ENTER)
wait(1)
# If the bmeirl account isnt logged in then log it in
if find("1476808553323.png"):
    wait(0.5)
    click("1476808565849.png")
    wait(0.5)
    click("1476808648459.png")
    # Delete any autofill stuff
    for x in range(0, 15):
        type(Key.BACKSPACE)
    type("bmeirl")
    click("1476808877272.png")
    click("1476808724678.png")
    for x in range(0, 15):
        type(Key.BACKSPACE)
    type("meirlbot")
    click("1476808910875.png")
    wait(5)
click("1476809108812.png")
click("1476809145474.png")
click("1476814856668.png")
type("000001.png")
type(Key.ENTER)
wait(3)
doubleClick("1476821718083.png")
click(Pattern("1476809223436.png").similar(0.16).targetOffset(-30,-136))
click(Pattern("1476809478219.png").similar(0.74))
wait(2)
for x in range(0,6):
    type(Key.DOWN)
wait(1)
#click(Pattern("1476809517773.png").targetOffset(-142,-2))
wait(2)
for x in range(0,9):
    type(Key.DOWN)
wait(2)
if(debug):
    click("1476809613850.png")