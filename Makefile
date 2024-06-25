c_name := "bot_instance"
i_name := "wkpnbot"


.PHONY: build
build:
	docker build --tag wkpnbot .


.PHONY: run
run:
	docker run -t -d --name $(c_name) --net=host -v /etc/letsencrypt:/etc/letsencrypt ${i_name}


.PHONY: cleanup
cleanup:
	docker rm -f $(c_name) && docker rmi $(i_name) && docker system prune -a -f


.PHONY: access_log
access_log:
	docker exec $(c_name) cat /var/log/nginx/access.log


.PHONY: error_log
error_log:
	docker exec $(c_name) cat /var/log/nginx/error.log
