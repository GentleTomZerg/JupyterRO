from roanno import cell, rocrate

# aaaaaa 
@cell 
def d():
    print("Process a")

@cell
def e():
    print("Process b")

@rocrate    
@cell
def f():
    print("Process c")
    e()    