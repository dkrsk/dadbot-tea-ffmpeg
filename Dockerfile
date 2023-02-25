FROM python:3.8.15-alpine
RUN apk update && apk upgrade && apk add ffmpeg opus && \
	apk add --update alpine-sdk && \
	apk add --update --no-cache --virtual .tmp-build-deps \
      build-base gcc python3-dev libffi-dev openssl-dev
COPY . ./app
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x ./init.sh
ENTRYPOINT ["./init.sh"]
#
