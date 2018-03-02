#!/bin/bash
#Author: Brian Rico
#Date: 02/18/2018
#Purpose: when the program runs, it will need arguments such as id to identify who is the
#the author of the program. It returns an error statement if the user entered no arguements.
#The program checks to see if the user specifies two directories that exist. Only there are issues
#that the program suns into when trying to see when the user enters the two directory names.

function id(){
    echo "program author: Brian Rico"
}

function usage(){
    ( >&2 echo "Error: myBackUp needs arguements
      Usage: myBackUp.sh id displayProgramAuthor
      myBackUp sourceDir destdir")
}

name='$[a-z]'
DATE=`date '+%a,%b %d at %M:%S'`

if [ $# = 0 ] ;
then
    echo "$(usage)"
    
elif [ $1 = "id" ];
then
    echo "$(id)"
    
elif [ $# = 2 ]; then
    if [ -d $1 ]; then
	if [ -d $2 ]; then
	    echo  "source: `"$1"`"
	    echo "Destination dir: `"$2"`"
	    echo "tar -cvf `"$1"`.tar `"$2"`"
	    echo "`tar name: ./`"$1"`.BK."DATE".tar`"
	    echo "`final name: ./`$1`.BK."DATE"`"
	    echo "`mv `$1`.tar new.tar`"
	    echo "`gzip $1new.tar`"
	else
	    (>&2 echo "The first directory does not exist")
	fi;
    else
	(>&2 echo "Sorry that directory does not exist either")
    fi;
else
    (>&2 echo "too many line arguements")
fi;


