#!/bin/bash

#Brian rico
#02/11/2018
#CPSC 434
#This program takes 3 arguements with the first being a number followed
#by an operator and then a number

#inputnum is set to any possible value between 0 and 9
#operator is set to any possible operator

#Exit 1 is when there isn't three arguements
#Exit 2 is when the user inputs an invalid operator
#Exit 3 is when the user inputs an invalid number for $1 and $3

#Bug1: the program does not seem to recognize '-' as one of the operators
#Bug2: the program does not seem to recognize '*' as one of the operators

inputnum='^[0-9]+$'
operator='^[+,-,*,/]$'

if [ "$#" != 3 ];
then
    echo "Error: program needs 3 inputs: number, operator, number"
    exit 1
else
    #checks to see if the user inputed numbers for the first input and third input
       if ! [[ "$1" =~ $inputnum ]] || !  [[ "$3" =~ $inputnum ]];
       then	   
	   echo "Error: first input needs to be a number"
	   echo "Error: third input needs to be a number"
	   exit 3
       fi;
       #checks to see if the user used one of the operators
	      if  ! [[ "$2" =~ $operator ]];
		then 
		    echo "Error: second input needs to be an operator [+, -, /, *]"
		    exit 2
	      else
		  operand=$2
	      fi;
fi;
#cases are used to check on which operand the user used to make a calculation
#could have done it with if-statements but this seemed more organized
case "$operand" in
    +)
	echo `expr "$1" + "$3"`	;;
    -)
	echo `expr "$1" - "$3"` ;;
    /)
	if ! [[ "$3" =~ 0 ]];
	then
	    #total="$input1" / "$input3"
	    #echo expr `"$total"`
	     echo `expr "$1" / "$3"`
	else
	    echo "Error: Division by zero - this does not make sense"	   
	fi;
	;;
    \*)
	echo `expr "$1" \* "$3"` ;;
esac
