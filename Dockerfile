FROM debian:stable-slim AS genbindings

WORKDIR "/build"

COPY . .

# Update apt database
RUN DEBIAN_FRONTEND=noninteractive apt update

# Install X11 headers
RUN DEBIAN_FRONTEND=noninteractive apt install -y libx11-dev

# Install python
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3

# Install C headers
RUN DEBIAN_FRONTEND=noninteractive apt install -y libc6-dev

# Install wget
RUN DEBIAN_FRONTEND=noninteractive apt install -y wget

# Install jextract
RUN wget https://download.java.net/java/early_access/jextract/21/1/openjdk-21-jextract+1-2_linux-x64_bin.tar.gz -O /opt/jextract.tgz
RUN tar -C /opt -xvf /opt/jextract.tgz

ENV PATH="/opt/jextract-21/bin:${PATH}"

# Generate bindings
RUN ./build.py generate

FROM debian:stable-slim AS package

WORKDIR "/build"

COPY --from=genbindings /build .

# Update apt database
RUN DEBIAN_FRONTEND=noninteractive apt update

# Install maven
RUN DEBIAN_FRONTEND=noninteractive apt install -y maven

# Install python
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3

# Install java jdk
RUN DEBIAN_FRONTEND=noninteractive apt install -y openjdk-21-jdk

# Package the JAR
RUN ./build.py package

ENTRYPOINT ["cp", "/build/target/javawm-1.0-SNAPSHOT-jar-with-dependencies.jar", "/output"]
