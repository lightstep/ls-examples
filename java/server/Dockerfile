FROM openjdk:8-jre-alpine

ADD target/server-1.0-SNAPSHOT.jar /app/
RUN wget -O /app/opentracing-specialagent-1.7.0.jar https://repo1.maven.org/maven2/io/opentracing/contrib/specialagent/opentracing-specialagent/1.7.0/opentracing-specialagent-1.7.0.jar

ENTRYPOINT java -javaagent:/app/opentracing-specialagent-1.7.0.jar  \
        -Dsa.tracer=lightstep \
        -Dls.componentName=$LIGHTSTEP_COMPONENT_NAME \
        -Dls.accessToken=$LIGHTSTEP_ACCESS_TOKEN \
        -Dls.collectorHost=$LS_COLLECTOR_HOST \
        -Dls.metricsUrl=$LS_METRICS_URL \
        -Dls.propagator=b3 \
        -cp /app/server-1.0-SNAPSHOT.jar \
        com.lightstep.examples.server.App
