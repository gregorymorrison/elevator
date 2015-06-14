#! /bin/python

import random

DEBUG = True

ITERATIONS = 5
MAX_PASSENGERS = 10
NEW_PSGR_CHANCE = .8
FLOORS = 10
ELEVATORS = 1
WAIT_TIME = 2
UP = 1;        DOWN = -1;        STILL = 0
OPEN = 1;    CLOSED = 0
ON = 1;        OFF = 0

floors = []; elevators = []; passengers = []

currfloors = [8, 1, 3, 9, 2, 1, 3, 2, 9, 5, 5, 6, 8, 5, 9, 2, 3, 3, 1, 6, 7, 6, 2, 9, 2, 4, 5, 8] 
destfloors = [2, 7, 7, 6, 8, 3, 0, 3, 0, 4, 2, 8, 4, 6, 6, 9, 2, 6, 3, 9, 8, 7, 1, 3, 3, 1, 7, 5]
els = [1, 9, 1, 2, 2, 6, 4, 9, 2, 1]

#-------------------------------------------------------------------------------

def gen_ID():
    x = 0
    while True:
        yield x
        x += 1
ID_gen = gen_ID()

#-------------------------------------------------------------------------------

class passenger:
    curr_floor = dest_floor = 0
    my_elevator = None

    def __init__(self):
        if DEBUG == True: print 'passenger.__init__'
        global floors

        self.ID = ID_gen.next()

        #randomly choose current and destination floors
        if DEBUG:
            self.curr_floor, self.dest_floor =  currfloors[0], destfloors[0]
        else:
            self.curr_floor = int(random.random()*FLOORS)
            self.dest_floor = int(random.random()*FLOORS)
        currfloors.remove(currfloors[0])
        destfloors.remove(destfloors[0])

        while self.dest_floor == self.curr_floor:
            if DEBUG:
                self.dest_floor = int(random.random()*FLOORS)
            else:
                self.dest_floor = int(random.random()*FLOORS)                

        self.push_btn()
    #def __init__(self):

    def push_btn(self):
        """
 routine to push floor button, if needed
 """
        if DEBUG == True: print self.ID, ' passenger.push_btn'
        bPushBtn = False

        #check the buttons first since it's a short routine
        if self.dest_floor > self.curr_floor:
            if floors[self.curr_floor].btn_up == OFF:
                bPushBtn = True
        elif self.dest_floor < self.curr_floor:
            if floors[self.curr_floor].btn_down == OFF:
                bPushBtn = True

        #next, check to see if an elevator is here
        for e in elevators:
            if e.curr_floor == self.curr_floor and e.door == OPEN:
                if self.dest_floor > self.curr_floor  and  e.direction <> DOWN:
                    if e.is_full <> False:
                        bPushBtn = False;    break

                elif self.dest_floor < self.curr_floor  and  e.direction <> UP:
                    if e.is_full <> False:
                        bPushBtn = False;    break
            #if e.curr_floor == self.curr_floor and e.door == OPEN:
        #for e in elevators:

        if bPushBtn == True:
            if self.dest_floor > self.curr_floor:
                floors[self.curr_floor].push_btn(UP)
            else:
                floors[self.curr_floor].push_btn(DOWN)
        #if bPushBtn == True:
    #def push_btn(self):

    def move(self):
        if DEBUG == True: print self.ID, ' passenger.move'
        global floors; global elevators

        #a person can be on an elevator...
        if self.my_elevator <> None:
            if self.curr_floor == self.dest_floor and self.my_elevator.door == OPEN:
                self.my_elevator.exit(self)

        else:
            #check to see if an elevator is here
            for e in elevators:
                if e.curr_floor == self.curr_floor and e.door == OPEN:
                    if self.dest_floor > self.curr_floor  and  e.direction <> DOWN:
                        #see if person can get on elevator
                        if e.board(self, self.dest_floor) == True:
                            self.my_elevator = e;    break

                    elif self.dest_floor < self.curr_floor  and  e.direction <> UP:
                        #see if person can get on elevator
                        if e.board(self, self.dest_floor) == True:
                            self.my_elevator = e;    break
                #if e.curr_floor == self.curr_floor and e.door == OPEN:
            #for e in elevators:

            if self.my_elevator == None:
                self.push_btn()
        #if self.my_elevator <> None:
    #def move(self):

    def render(self):
        pass
    #def render(self):
#class passenger:

#-------------------------------------------------------------------------------

class elevator:
    curr_floor = 0
    time_left = WAIT_TIME
    door = OPEN
    direction = STILL

    def __init__(self, ID):
        if DEBUG == True: print 'elevator.__init__'
        self.ID = ID
        self.riders = [];    self.btns_pushed = []
        if DEBUG == True:
            self.curr_floor = els[0]
        else:
            self.curr_floor = int(random.random()*FLOORS)
        els.remove(els[0])
    #def __init__(self, ID):

    def is_full(self):
        return len(self.riders) == MAX_PASSENGERS

    def board(self, rider, dest_floor):
        """
		public function a passenger can call to attempt to board an elevator
		"""
        if DEBUG == True: print self.ID, ' elevator.board'
        retval = False

        if self.door == OPEN  and  len(self.riders) < MAX_PASSENGERS:
            self.riders.append(rider)
            if rider.dest_floor < rider.curr_floor:
                self.direction = DOWN
            else:
                self.direction = UP

            try:
                temp = self.btns_pushed.index(dest_floor)
            except:
                self.btns_pushed.append(dest_floor)
            self.btns_pushed.sort()
            retval = True

        return retval
    #def board(self, ID):

    def exit(self, rider):
        """
		public function for a passenger to exit elevator
		"""
        if DEBUG == True: print self.ID, ' elevator.board'

        for r in self.riders:
            if r.ID == rider.ID:
                self.riders.remove(r);    break
        #for r in self.riders:
    #def exit(self, rider):

    def __check_floors(self, direction):
        """
		check to see if there are floors with buttons pushed in the right direction
		"""
        if DEBUG == True: print self.ID, ' elevator.__check_floors'
        global floors

        retval = False

        for f in floors:
            if direction == UP:
                if f.ID > self.curr_floor  and  (f.btn_down == ON or f.btn_up == ON):
                    retval = True;    break

            else:
                if f.ID < self.curr_floor  and  (f.btn_down == ON or f.btn_up == ON):
                    retval = True;    break
        #for f in floors:

        return retval
    #def __check_floors(self, direction):

    def __choose_direction(self):
        """
		checks to see if anyone wants to use the elevator
		sets new floor, direction, and door open status
		"""
        if DEBUG == True: print self.ID, ' elevator.__choose_direction'
        global floors
        bRideRequested = bUpRequested = bDownRequested = bOutRequested = bInRequested = False

        if len(self.riders) > 0:
            #look to see if any people on the elevator want to go anywhere
            for rider in self.riders:
                if rider.curr_floor <> rider.dest_floor:
                    bRideRequested = True;
                if rider.curr_floor > rider.dest_floor:
                    bDownRequested = True
                elif rider.curr_floor < rider.dest_floor:
                    bUpRequested = True
                elif rider.curr_floor == rider.dest_floor:
                    bOutRequested = True
            #for rider in self.riders:

            #also check the floor to see if anyone is here waiting
            if floors[self.curr_floor].btn_up == True and self.direction == UP:
                bInRequested = bUpRequested = True
            elif floors[self.curr_floor].btn_down == True and self.direction == DOWN:
                bInRequested = bDownRequested = True

        else:
            #check all the floors and see if anyone else wants a ride
            for f in floors:
                if f.btn_up == ON or f.btn_down == ON:
                    bRideRequested = True;
                    if f.ID > self.curr_floor: 
                        bUpRequested = True
                    elif f.ID < self.curr_floor: 
                        bDownRequested = True
                    elif f.ID == self.curr_floor:
                        #pick a person up if we're not traveling in the other direction
                        if (f.btn_down and self.direction <> UP)  or  \
                                (f.btn_up and self.direction <> DOWN):
                            bInRequested = True
                            if f.btn_down:
                                bDownRequested = True
                            elif f.btn_up:
                                bUpRequested = True
            #for f in floors:
        #if len(self.riders) > 0:

        if bRideRequested == False:
            self.direction = STILL
            self.door = OPEN

        else:
            if bInRequested  or  bOutRequested:
                #open the door for the people and change direction accordingly
                self.door = OPEN
                if bUpRequested and bDownRequested:
                    if self.direction == STILL:
                        self.direction = UP
                elif bUpRequested:
                    self.direction = UP
                elif bDownRequested:
                    self.direction = DOWN

            else:
                self.door = CLOSED

                if self.curr_floor == 0  or  \
                        (self.direction <> DOWN and bUpRequested):
                    self.curr_floor += 1
                    if self.curr_floor == FLOORS-1:
                        self.direction = DOWN
                    else:
                        self.direction = UP

                elif self.curr_floor == FLOORS-1  or  \
                        (self.direction <> UP and bDownRequested):
                    self.curr_floor -= 1
                    if self.curr_floor == 0:
                        self.direction = UP
                    else:
                        self.direction = DOWN
            #if bThisRequested:
        #if bRideRequested == False:
    #def choose_direction(self):

    def move(self):
        global floors
        if DEBUG == True: print self.ID, ' elevator.move'

        bStay = True
        if self.door == OPEN:
            #turn off the button on this floor
            if self.direction <> DOWN:
                floors[self.curr_floor].btn_up = OFF
            if self.direction <> UP:
                floors[self.curr_floor].btn_down = OFF

            #decide whether to stay or leave 
            if self.time_left <= 0:
                if self.__check_floors(DOWN) == True and self.direction <> UP:
                    bStay = False
                elif self.__check_floors(UP) == True and self.direction <> DOWN:
                    bStay = False
            #if len(self.riders) == MAX_PASSENGERS

            #if anyone is waiting for a ride, then keep counting the timer,
            bRideRequested = False
            for f in floors:
                if f.btn_down == ON  or  f.btn_up == ON:
                    bRideRequested = True;     break

            if bStay:
                #sit and wait another time unit
                if self.riders <> [] or bRideRequested:
                    #if anyone has gotten aboard, start the door clock
                    self.time_left -= 1
                else:
                    self.time_left = WAIT_TIME

            else:
                #take off
                self.door = CLOSED
                self.time_left = WAIT_TIME                
                self.__choose_direction()
            #if bStay:

        else:
            self.__choose_direction()
        #if self.door == OPEN:

        #now consider what happens after elevator has moved
        if self.door == OPEN:
            #elevator did nothing during this turn
            if self.direction == STILL:
                floors[self.curr_floor].btn_up = OFF
                floors[self.curr_floor].btn_down = OFF
                self.time_left = WAIT_TIME

        else:    #self.door == CLOSED
            #the elevator has just moved, so decide what to do next
            self.time_left = WAIT_TIME

            #check to see if this floor was requested if we've moved this round
            bRiderWantsOut = False
            try:
                temp = self.btns_pushed.index(self.curr_floor)
                bRiderWantsOut = True
                self.door = OPEN
            except:
                pass    #nobody wants out

            #see if there are any more requests for rides
            #if nobody wants to get out, we may have moved to a floor where someone wants a ride
            #but we have to ignore them if we're going in the opposite direction
            #or if there's someone past them that we have to pick up first
            bRideRequested = bThisFloorRequested = False

            for f in floors:
                #if someone here or higher wants to go down and there is noone above them that wants to
                if f.ID >= self.curr_floor and f.btn_down == ON and self.direction <> DOWN:
                    bDontStop = False
                    for f1 in floors[f.ID+1:]:
                        if f1.ID > f.ID  and  f.btn_down == ON:
                            bDontStop = True;    break
                    if bDontStop == False:
                        self.direction = UP
                        bRideRequested = True
                        if f.ID == self.curr_floor:
                            bThisFloorRequested = True
                        break

                #if someone here or lower wants to go down
                if f.ID <= self.curr_floor and f.btn_down == ON and self.direction <> UP:
                    self.direction = DOWN
                    bRideRequested = True
                    if f.ID == self.curr_floor:
                        bThisFloorRequested = True
                    break

                #if someone here or lower wants to go up and there is noone below them that wants to
                if f.ID <= self.curr_floor and f.btn_up == ON and self.direction <> UP:
                    bDontStop = False
                    for f1 in floors[:f.ID]:
                        if f1.ID < f.ID  and  f.btn_up == ON:
                            bDontStop = True;    break
                    if bDontStop == False:
                        self.direction = DOWN
                        bRideRequested = True
                        if f.ID == self.curr_floor:
                            bThisFloorRequested = True
                        break

                #if someone here or higher wants to go up
                if f.ID >= self.curr_floor and f.btn_up == ON and self.direction <> DOWN:
                    self.direction = UP
                    bRideRequested = True
                    if f.ID == self.curr_floor:
                        bThisFloorRequested = True
                    break
            #for f in floors:

            if bRideRequested:
                if bThisFloorRequested:
                    self.door = OPEN
            else:
                if len(self.riders) == -1:
                    self.direction = STILL

            #turn off the floor light if the door is open to let people on
            if self.door == OPEN:
                if self.direction == UP:
                    floors[self.curr_floor].btn_up = OFF
                if self.direction == DOWN:
                    floors[self.curr_floor].btn_down = OFF
        #if bStay == False:

        #finally, set curr_floor for all passengers
        for r in self.riders:
            r.curr_floor = self.curr_floor
    #def consider_move(self):

    def render(self):
        line = 'elevator: floor ' +  str(self.curr_floor) + ', '
        if self.direction == 1: line += 'going UP, '
        elif self.direction == 0: line += 'STILL, '
        else: line += 'going DOWN, '
        line += 'time: ' + str(self.time_left) + ' '
        line += self.door and 'OPEN: [' or 'CLOSED: ['
        line += ','.join([str(r.dest_floor) for r in self.riders]) + ']'
        print line
    #def render(self):
#class elevator:

#-------------------------------------------------------------------------------

class floor:
    btn_up = btn_down = OFF

    def __init__(self, ID):
        if DEBUG == True: print 'floor.__init__ '
        self.ID = ID
    #def __init__(self, ID):

    def push_btn(self, direction):
        if DEBUG == True: print self.ID, ' floor.push_btn ', direction
        if direction == UP:
            self.btn_up = ON
        elif direction == DOWN:
            self.btn_down = ON
    #def push_btn(direction):

    def render(self):
        print 'floor ', self.ID, ':', self.btn_up and 'UP ' or ' ', self.btn_down and 'DOWN' or ''
    #def render(self):
#class floor:

#-------------------------------------------------------------------------------

class simulation:
    def __init__(self):
        if DEBUG == True: print 'simulation.__init__ '
        global floors; global elevators; global passengers

        floors = [floor(i) for i in range(FLOORS)]
        elevators = [elevator(i) for i in range(ELEVATORS)]
    #def __init__(self):

    def run(self):
        if DEBUG == True: print 'simulation.run'
        global elevators; global passengers

        self.render()

        for i in range(ITERATIONS):
            #randomly add a person to the sim
            #if random.random() <= NEW_PSGR_CHANCE:
            passengers.append(passenger())

            to_remove = []
            for i in range(len(passengers)-1, -1, -1):
                p = passengers[i]
                p.move()
                if p.dest_floor == p.curr_floor:
                    to_remove.append(i)

            for i in to_remove:
                passengers.remove(passengers[i])

            print 'people move\n'; self.render()

            for e in elevators:    e.move()

            print 'elevators move\n'; self.render()
        #for i in ITERATIONS:
    #def run(self):

    def render(self):
        if DEBUG == True: print 'simulation.render'
        global floors; global elevators; global passengers

        print 'people: ' + ', '.join([p.my_elevator and 
                '['+str(p.curr_floor)+'-'+str(p.dest_floor)+']' or
                str(p.curr_floor)+'-'+str(p.dest_floor)  
                for p in passengers])

        for e in elevators:    e.render()

        for f in floors[::-1]:    f.render()

        print '\n'
    #def render(self):
#class simulation(): 

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    import os, pdb
    if os.environ.has_key('PROMPT'): pdb.set_trace()

    sim = simulation()
    sim.run()