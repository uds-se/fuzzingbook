echo '(Re)starting container with interactive notebook'

if docker ps | grep 'fuzzing-book-instance'; then
	docker stop fuzzing-book-instance
	docker start fuzzing-book-instance
else
	docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book
fi


echo 'Open this URL in your browser to access the notebook:'
docker logs -f --since=5m fuzzing-book-instance