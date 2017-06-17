#!python3
#boss_class.py is a script to demo Python Classes and Subclasses

class Boss(object):
    def __init__(self, name, attitude, behaviour, face):
        self.name = name
        self.attitude = attitude
        self.behaviour = behaviour
        self.face = face
    
    def get_attitude(self):
        return self.attitude
    
    def get_behaviour(self):
        return self.behaviour
    
    def get_face(self):
        return self.face

class GoodBoss(Boss):
    def __init__(self,
                name,
                attitude,
                behaviour,
                face):
        super().__init__(name, attitude, behaviour, face)
        
    def nurture_talent(self):
        #A good boss nurtures talent making employees happy!
        print("The employees feel all warm and fuzzy then put their talents to good use.")
    
    def encourage(self):
        #A good boss encourages their employees!
        print("The team cheers, starts shouting awesome slogans then gets back to work.")


class BadBoss(Boss):
    def __init__(self,
                name,
                attitude,
                behaviour,
                face):
        super().__init__(name, attitude, behaviour, face)

    def hoard_praise(self):
        #A bad boss takes all the praise for him/herself
        print("The employees feel cheated and start plotting {}'s demise while he stares at his own reflection.".format(self.name))
        
    def yell(self):
        #A bad boss yells! (Ain't nobody got time for that!)
        print("Everyone stares while {} yells. Someone shouts, 'Won't somebody PLEASE think of the children!'".format(self.name))
        print("{} storms off, everyone comforts the victim and one person offers to arrange an 'accident' for {}.".format(self.name, self.name))