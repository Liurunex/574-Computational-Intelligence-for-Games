CXX = g++
CXXFLAGS = -Wall -pedantic -std=c++11

Pig: Pig.o
	${CXX} ${CXXFLAGS} -o Pig Pig.o

Pig.o: Pig.cpp
	${CXX} ${CXXFLAGS} -c Pig.cpp

clean:
	$(RM) Pig *.o
