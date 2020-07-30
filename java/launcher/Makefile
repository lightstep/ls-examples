.PHONY: build clean

agent_url := https://github.com/lightstep/otel-launcher-java/releases/download/v0.0.1-alpha/lightstep-opentelemetry-javaagent-0.1.0-SNAPSHOT.jar

build: lightstep-opentelemetry-javaagent-0.1.0-SNAPSHOT.jar
	mvn package -f pom-server.xml
	mvn package -f pom-client.xml

lightstep-opentelemetry-javaagent-0.1.0-SNAPSHOT.jar:
	wget ${agent_url}

clean:
	mvn clean -f pom-server.xml
	mvn clean -f pom-client.xml
