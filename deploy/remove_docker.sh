read -p "This will remove all the docker remnants of your fuzzing book installation. Continue? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker stop fuzzing-book-instance
    docker rm fuzzing-book-instance
    docker rmi fuzzing-book
fi