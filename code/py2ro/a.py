from roanno import cell
from b import d, e, f

# This is method a
# it prints Process a
@cell 
def a():
    print("Process a");

@cell
def b():
    print("Process b");

# This is method c    
@cell
def c():
    print("Process c");
  

# # def b():
# #     print("Process b");
if __name__ == "__main__":
    a()
    b()
    c()
    d()
    e()
    f()