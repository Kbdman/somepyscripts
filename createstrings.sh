dict=("Q" "W" "E" "R" "T" "Y" "U" "I" "O" "P" "A" "S" "D" "F" "G" "H" "J" "K" "L" "Z" "X" "C" "V" "B" "N" "M" "q" "w" "e" "r" "t" "y" "u" "i" "o" "p" "a" "s" "d" "f" "g" "h" "j" "k" "l" "z" "x" "c" "v" "b" "n" "m" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9")
len=5
i=0
while [ $i -lt $len ]
do
    #out[$i]=${dict[0]}
    index[$i]=0
    ((i++))
done
last_index=`expr $len - 1`
max_index=`expr ${#dict[@]} - 1`
idxlen=`expr ${#index[@]} - 1`
while [ 0 -lt 1 ]
do
    found=0
    k=$idxlen
    while [ $k -ge 0 ] 
    do 
        #echo ${index[$k]}
        #echo $max_index
        if  [ ${index[$k]} -lt $max_index ] 
        then
            index[$k]=`expr ${index[$k]} + 1`
            j=`expr $k + 1`
            while [ $j -le $idxlen ]
            do
                index[$j]=0
                ((j++))
            done
            found=1
            echo ${dict[${index[0]}]}${dict[${index[1]}]}${dict[${index[2]}]}${dict[${index[3]}]}${dict[${index[4]}]}
            break
        fi
        ((k--))
    done
    if [ $found -eq 0 ]
    then 
        break
    fi
done

