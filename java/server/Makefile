.PHONY: build clean

specialagent_url := https://repo1.maven.org/maven2/io/opentracing/contrib/specialagent/opentracing-specialagent/1.7.0/opentracing-specialagent-1.7.0.jar

build: opentracing-specialagent-1.7.0.jar
	mvn package

opentracing-specialagent-1.7.0.jar:
	wget ${specialagent_url}

clean:
	mvn clean
