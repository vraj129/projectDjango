# RED='\033[0;31m'
echo -e "\e[1;33m"  # Changing Color
echo "If possible, run this script in an Empty folder. Do not forget to copy \`collection.txt\` to that folder"
echo -e "\e[1;33m"  # Changing Color
# echo -e "\e[1;31m"  # Changing Color
printf "OR\nMake sure this Directory has no important files or folder. It may override filenames based on the name of your collection name\n"
echo -en "\e[0m"  # Changing Color Back
echo "Press y to continue anyway"
read choice
if [[ $choice != "y" ]];then
    echo "Exiting"
    exit 1
fi

change_directory=0
go_back=0
i=1
while read line; do    
    # If Starts with -(wildcard matching)
    if [[ $line == -* ]]; then
        printf "\n$line\n"
        if [[ -d ${line:1} ]]; then
            # echo "$line Directory exists"
            :
        else
            mkdir ${line:1}
            # echo "$line Directory created"
        fi
        lastread_directory_name=${line:1}
        change_directory=1
    else
        # echo "Not Starts with -"
        if [[ $change_directory == 1 && $go_back == 1 ]]; then
            cd ..
            cd $lastread_directory_name
            echo "Changed Directory"
            pwd
        elif [[ $change_directory == 1 && $go_back == 0 ]]; then
            echo "Changed Directory"
            cd $lastread_directory_name
            go_back=1
            pwd
        fi
        echo "Creating Backup for \"$line\" ... "
        mongoexport --uri mongodb+srv://ajinzrathod:ajinz812@theunitedcodes.eump1.mongodb.net/$lastread_directory_name --collection $line --type json --out $line.json
        echo "Done"
        change_directory=0
        ((i++))
        # touch $i
    fi
done < collections.txt
# mongoexport --uri mongodb+srv://ajinzrathod:ajinz812@theunitedcodes.eump1.mongodb.net/tuc --collection  --type <FILETYPE> --out <FILENAME>
