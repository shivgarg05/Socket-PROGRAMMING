import socket
import sys
import time
import select
import random


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 5006

s.bind((host, port))
s.listen(100)
def making_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]
    j=0
    while True:
            connection, address = s.accept()
            s.setblocking(1)
            j=j+1
            all_connections.append(connection)
            all_address.append(address)
            if j<4:
               
                print("Connection has been established")
                connection.send(str.encode("Total questions are 10. First one to reach 5 points wins.First enter yes for buzzer and then answer the question.If you don't know the question just don't press buzzer"))
                time.sleep(1)
                connection.send(str.encode("You are Player : "+ str(j)))
                time.sleep(1)
                connection.send(str.encode("Welcome to the game\n"))
                connection.send(str.encode("Press 'Y' or 'y' for buzzer"))

                if j==3:
                	ques_ans()
                	break;

all_connections = []
all_address = []
Questions=[" What is the capital of France? \n a.New Delhi b.Paris c.Rome d.Venice",
     " Who was India's first female Prime Minister ?\n a.Jay Lalitha b.Indira Gandhi c.Sushma Swaraj d.Rajiv Gandhi",
     " Which is the largest country in the world ?\n a.USA b.Russia c.Australia d.Brazil",
     " How many states are there in India? \n a.24 b.29 c.28 d.31",
     " Which planet is closest to the sun? \n a.Mercury b.Pluto c.Earth d.Venus",
     " What is the currency of Japan? \n a.Ruble b.Yuan c.Japanese Dollar d.Yen",
     " In which country is Timbuktu? \n a.Ethiopia b.Uganda c.Mali d. Egypt",
     " Who invented Television? \n a.John Logie Baird b.AG Bell c.Nikola Tesla d.Martin Cooper",
     " Where is Swaziland? \n a. Asia b. South America c. Europe d. Africa",
     " Which Indian state is know as the 'Land of 5 rivers'?\n a.Punjab b. Rajasthan c. Andhra Pradesh d. Maharashtra",
     " Corey Anderson who has hit the fastest ODI century in 36 balls is from \n a.England b.Australia c.West Indies d.New Zealand",
     " The world smallest country is \n a. Canada b. Russia c. Maldives d. Vatican City ",
     " Novak Djokovic is a famous player associated with the game of\n a.Cricket b. Football c. Lawn Tennis d. Hockey",
     " Which one of the following was the first fort constructed by the British in India?\n a. Fort William b. Fort St.George c. Fort St. David d. Fort St.Angelo",
     " Which language is spoken in Karnataka?\n a.Punjabi b.Marathi c.Kannada d.Bengali",
     " The state which has the largest number of sugar mills in India is\n a.Uttar Pradesh b.Punjab c.Harayana d.Madhya Pradesh",
     " The currency notes are printed in\n a.New Delhi b.Nasik c.Nagpur d.Bombay",
     " What is the world's most common religion?\n a.Hinduism b.Sikhism c.Christianity d.Islam",
     " Durand Cup is associated with the game of\n a.Cricket b.Football c.Hockey d.Volleyball",
     " Entomology is the science that studies\n a.Behaviour of human beings b.Insects c.The origin and history of technical and scientific terms d.The formation of rocks"
     ]
Answers=['b', 'b', 'b', 'c', 'a', 'd','c', 'a', 'd', 'a', 'd', 'd', 'c', 'b', 'c', 'a', 'b', 'c', 'b','b']
Marks=[0,0,0]
response=[]    
def ques_ans():

	i=1
	while True:
		i = random.randint(0,10000)%len(Questions)
		for connection in all_connections:
			time.sleep(0.5)
			connection.send(str.encode(Questions[i]))
		response1 = select.select(all_connections,[],[],20)
		if(len(response1[0])>0):
			connection_name = response1[0][0];
			k = connection_name.recv(2048)
			k = k.decode("utf-8")
			response1 = ()
			for connection in all_connections:
				if connection != connection_name:
					connection.send(str.encode("Player "+str(all_connections.index(connection_name)+1)+ " pressed the buzzer first."))
			for p in range(len(all_connections)):
					if all_connections[p]==connection_name:
						t=p;
			if k=='y' or k=='Y':
				connection_name.send(str.encode("Answer the Question"))
				answer=str(connection_name.recv(1024),"utf-8")
				if answer==str(Answers[i]):
					Marks[t]=Marks[t]+1
					connection_name.send(str.encode("Correct Answer, +1 points"))
					if Marks[t]>=5:
						for c in all_connections:
							c.send(str.encode("Over"))
							time.sleep(1)
						break

				else:
					Marks[t]=Marks[t]-0.5
					connection_name.send(str.encode("Wrong Answer, -0.5 points"))

		else:
			for c in all_connections:
				c.send(str.encode("Nobody pressed the buzzer.Moving on to the next question"))
		if i==len(Questions):
			for c in all_connections:
				c.send(str.encode("Over"))
				time.sleep(1)			
			break
		else:
			Questions.pop(i)
			Answers.pop(i)
			i = i+1
			


def main():
    making_connections()
    y=0
    d=0
    for i in range(len(all_connections)):
        if Marks[i]>y:
            d=i
            y=Marks[i]
    for c in all_connections:
        if all_connections.index(c)!=d:
            c.send(str.encode("The winner is Player: " + str(d+1)+" with "+str(y)+" Points" ))
        else:
            c.send(str.encode("Congratulations! You are the winner with " + str(y)+" Points" ))
        
main()