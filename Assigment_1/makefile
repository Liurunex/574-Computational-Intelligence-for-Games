CXX = g++
CXXFLAGS = -Wall -pedantic -std=c++11

Kayles.16: Kayles.o
	${CXX} ${CXXFLAGS} -o Kayles.16 Kayles.o

Kayles.o: Kayles.cpp
	${CXX} ${CXXFLAGS} -c Kayles.cpp

clean:
	$(RM) Kayles.16 *.o
