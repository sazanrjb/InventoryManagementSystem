import time as t

class Body():
     def __init__(self,start,speed,length= 0):
         self.sx = start
         self.dx = speed
         self.born = t.time()
         self.length = length

     def __setitem__(self, key, item):
         self.key = item
         
     def distance(self,time):
         return time*self.dx
        
     def get_x(self):
         self.diff = t.time() - self.born
         self.x = self.sx + (self.diff*self.dx)
         return round(self.x,3)
             
     def stime(self,obj2):
         x = self.get_x()
         y = obj2.get_x()
         r=0
         print x,"km",y,"km" ,"in" , round(x/self.dx)
         if self.dx>obj2.dx :
             return "cannot catch the other object"
         while x>y:
             r = r+1
             x = self.get_x()
             y = obj2.get_x()
         print round(r/obj2.diff),"Frames per second"
         print x,"km",y,"km" ,"in" , round(y/obj2.dx,3) ,"Hour"
         return y/obj2.dx
      
     def otime(self,obj2):
         obj2.dx = -obj2.dx
         x = self.get_x()
         y=  obj2.get_x()
         r = 0
         print x,"km",y,"km" ,"in" , x/self.dx
         while y>x :
             r= r +1
             x = self.get_x()
             y= obj2.get_x()
         print round(r/obj2.diff),"Frames per second"
         print x ,"km",y,"km","in",round(obj2.diff,3),"Hour"
         return obj2.diff
         
     def Passtime(self,obj2,opposite = True):
         if opposite == True:
             relative = obj2.dx + self.dx
         elif obj2.dx==self.dx:
             print "Both objects are at same speed "
             return None
         else :
             relative = obj2.dx - self.dx
         ptime = self.length/(relative*(5.0/18))
         return ptime
         
     
Train1 = Body(0,40.0)
Train2 = Body(0,60.5)

     
         
         
         
   




