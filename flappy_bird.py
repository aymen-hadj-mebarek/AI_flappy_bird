import pygame,neat,time,os,random,math

# setting the window width and height
WIN_WIDTH = 550
WIN_HEIGHT = 800
MAX_VEL = 25
USED_VEL = 5
gen = 1
# initialization the font for the score
pygame.font.init()
Font = pygame.font.SysFont("comicsans",50)
Font2 = pygame.font.SysFont("comicsans",20)
# Importing the images

# the bird images to make it look like moving
# scale2x : is used to make the image bigger
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
# the Pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
# the Base (floor) image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
# the Background image
BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

# creating the classes for the object of the game : (bird, pipe, base)
''' BIRD CLASS '''
class Bird:
    IMGS = BIRD_IMGS    # making importing the images easier
    MAX_ROT = 25    # max rotation that the bird can rotate when jumping or falling
    ROT_VEL = 20    # rotation velocity how the bird will rotate each frame
    ANIM_TIME = 5   # animation time
    
    def __init__(self,x,y):
        # x and y are the starting coordinates of the bird
        self.x = x
        self.y = y
        self.tilt = 0       # the bird will start at angle 0 and then start rotating
        self.tick_count = 0 # number of clicks (used to know how high the bird has to be ... physical stuff )
        self.vel = 0        # the moves of the birs start at 0
        self.height = y     # the height of the bird is the same as its y position
        self.img_count = 0  # to keep tracking the animation of the bird as it moves
        self.img = self.IMGS[0]  # the starting frame wil be the first picture in the IMGS array
        
    def jump(self):
        self.vel = -10.5    # we give a negative number bcs the O(0,0) coordinates of pygame is in the top left corner
        self.tick_count = 0
        self.height = self.y
        
    def move(self): 
        # this will called every frame to give the animation of the bird
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*(self.tick_count**2)         # how many pixels we are moving (acceleration)
        
        if d >= 16 :    # limiting the fall speed to 16px per frame
            d = 16
        elif d<0:       # we can change this to make the jump higher or lower 
            d -= 2

        self.y += d     # changing the y position by the "d" value
        
        if d<0 or self.y < self.height +20:     
            # seeing if the birs is still jumping (d<0) or just falling from the jump ..  he will still look up when starting to fall
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT    # making the bird looks up while jumping
        else:
            if self.tilt > -90:
                self.tilt -= self.MAX_ROT   # making the bird rotate slowly til its 90° down
    
    def draw(self,win):     # win : is the window we are drawing in
        self.img_count += 1
        # this is responsible for the wings to flap
        if (self.img_count < self.ANIM_TIME):
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIM_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIM_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIM_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIM_TIME*4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        if self.tilt <= -80:    # when he's falling it doesn't matter if he flap his wings
            self.img = self.IMGS[1]
            self.img_count = self.ANIM_TIME*2
            
        # making the bird tilt and rotate
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)   
        # draswing the image in the window
        win.blit(rotated_image,new_rectangle.topleft)
        
    def get_mask(self):         # used in collision
        # the mask is the array of picxels that are occupied in the square of the image .. it helps get more accurate collision detection
        return pygame.mask.from_surface(self.img)
   
''' PIP CLASS ''' 
class Pipe:
    GAP = 200
    # VEL = 5
     
    def __init__(self,x,vel):
        self.x = x
        self.height = 0
        self.VEL = vel
        self.top = 0
        self.bottom = 0
        self.PIP_TOP = pygame.transform.flip(PIPE_IMG,False,True)   # read the parameters
        self.PIP_BOTTOM = PIPE_IMG
        
        self.passed = False     # if the bird has passed by the pipe or not
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(40,450)
        self.top = self.height - self.PIP_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL
        
    def draw(self,win):
        win.blit(self.PIP_BOTTOM,(self.x,self.bottom))
        win.blit(self.PIP_TOP,(self.x,self.top))
        
    def collide(self,bird):
        bird_mask = bird.get_mask()
        TOP_MASK = pygame.mask.from_surface(self.PIP_TOP)
        BOTTOM_MASK = pygame.mask.from_surface(self.PIP_BOTTOM)
        
        # calculing the offset: the offset is the distance between 2 object
        top_offset = (self.x - bird.x , self.top - round(bird.y)) 
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        # seeing if the objects collide
        x_point = bird_mask.overlap(BOTTOM_MASK,bottom_offset) # if the objects dont collide it will return None
        y_point = bird_mask.overlap(TOP_MASK,top_offset)
        
        if x_point or y_point:
            return True
        else:
            return False
        
''' BASE CLASS '''
class Base:
    VEL = 5     # it has to be the same as the velocity of the pipe so they move in the same time
    WIDTH = BASE_IMG.get_width( )
    IMG = BASE_IMG
    
    def __init__(self,y):
        self.y = y
        self.x1 =  0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        if (self.x1 + self.WIDTH < 0):
            self.x1 = self.x2 + self.WIDTH
        
        if (self.x2 + self.WIDTH < 0):
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
        
        
def draw_window(win,birds,pipes,base,score,gen):  
    # blit = draw
    win.blit(BACKGROUND,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    for bird in birds:
        bird.draw(win)
    base.draw(win)
    text = Font.render("score : "+str(score),1,(255,255,255))
    nbr = Font2.render("Remaining : "+str(len(birds)),1,(255,255,255))
    gen = Font2.render("Generation : "+str(gen),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-text.get_width(),0))
    win.blit(nbr,(0,0))
    win.blit(gen,(0,nbr.get_height()+10))
    pygame.display.update()
    

# to give the main as a parameter to the model we have to give it some arguments : (genomes,config)
def main(genomes,config):
    USED_VEL = 5
    global gen 
    score = 0
    nets = []
    ge = []
    birds = []
    
    for _,g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(125,300))
        ge.append(g)
        
        
    base = Base(700)
    pipes = [Pipe(550,USED_VEL)]
    window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    run = True
    
    # were are making the clock to limit the frames and the time so it doesn't go faster than its supposed to go
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(30)      # witout this clock command the game will run so fast you cant see it good 
                            # we limited the clock on the 30 ticks so it will wait for 30 ticks to run the animation 
        for event in pygame.event.get():
            # if event.type == pygame.KEYUP:
            #     birdie.jump()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
    
        # moving the birds by the neural network
        
        # checking which pipe the bird has to look out for to know how to move and jump
        pipe_ind = 0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x> ((pipes[0].x + pipes[0].PIP_TOP.get_width())* 3/4):
                pipe_ind = 1
        else:
            run = False
            gen += 1
                
        for x,birdie in enumerate(birds):   # we will check the value given by the neural network and if its greater than 5 then the bird will jump
            birdie.move()
            ge[x].fitness += 0.1
            
            output = nets[x].activate((birdie.y,abs(birdie.y - pipes[pipe_ind].height),abs(birdie.y - pipes[pipe_ind].bottom)))
            if (output[0] > 0.5):
                birdie.jump()
            
        
        add_pipe = False
        rem = []        # this is a list for removed pipes
        for pipe in pipes:
            pipe.move()
            for x,birdie in enumerate(birds):
                if (pipe.collide(birdie)):
                    ge[x].fitness -= 1  # making the fitness smaller so it will be considdered as worst specie in the model
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
            # generating new pipes each time a pipe leave the screen
            if (pipe.x + pipe.PIP_BOTTOM.get_width() < 0):
                # USED_VEL = USED_VEL + 0.02
                rem.append(pipe)
                        
            if not pipe.passed and pipe.x < birdie.x:
                pipe.passed = True
                add_pipe = True

            


        # adding to the score and making a new pipe
        if add_pipe:
            score += 1 
            for g in ge:
                g.fitness += 4                
            pipes.append(Pipe(550,USED_VEL))
            if USED_VEL < MAX_VEL:
                USED_VEL = USED_VEL + 0.5
        # removing the old pipes so it doesnt lag
        for r in rem:
            pipes.remove(r)
            pipe_ind = 0
        for x,birdie in enumerate(birds):
            if birdie.y + birdie.img.get_height() > 700 or birdie.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        base.move()
        draw_window(window,birds,pipes,base,score,gen)
                
    print("score : ",score)
    
# main()

# running the NEAT model :
# defining the function to run neat model with the default parameters
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    population = neat.Population(config)
    # adding the stat reporter (not necessary)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    winner = population.run(main,20)        # 50 is the number of generations
    # we are passing the main function to the model so it will test on it for 50 generation
    
    
# runnint he model on the main program
if __name__ == '__main__':
    local_dire = os.path.dirname(__file__)
    config_path = os.path.join(local_dire,"NEAT_config.txt")
    run(config_path)