FROM apache/airflow:2.5.0-python3.8
RUN python -m ensurepip --upgrade
RUN pip install --no-cache-dir textblob pmdarima matplotlib seaborn statsmodels scikit-learn catboost selenium pyspark==3.2.3
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark \
    && pip freeze

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
#ARG AIRFLOW_HOME=/usr/local/airflow
ARG SPARK_VERSION="3.2.3"
ARG HADOOP_VERSION="3.2"

#RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow
USER root
#RUN rm -rf \
        #/var/lib/apt/lists/* \
        #/tmp/* \
        #/var/tmp/* \
       # /usr/share/man \
      #  /usr/share/doc \
     #   /usr/share/doc-base \
# Java is required in order to spark-submit work
# Install OpenJDK-8
RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        iputils-ping \
        telnet
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y gnupg2 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB9B1D8886F44E2A && \
    add-apt-repository "deb http://security.debian.org/debian-security stretch/updates main" && \ 
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    java -version $$ \
    javac -version
RUN apt-get install python3
RUN python3 --version
RUN which python3
# Setup JAVA_HOME 
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME
###############################
## Finish JAVA installation
###############################

ENV SPARK_HOME /opt/spark

# Spark submit binaries and jars (Spark binaries must be the same version of spark cluster)
RUN apt-get install wget
RUN cd "/tmp" && \
        wget --no-verbose "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
        tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
        mkdir -p "${SPARK_HOME}/bin" && \
        mkdir -p "${SPARK_HOME}/assembly/target/scala-2.12/jars" && \
        cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
        cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.12/jars/" && \
        rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"
        
#RUN chown -R airflow: ${AIRFLOW_HOME}

# Create SPARK_HOME env var
RUN export SPARK_HOME
ENV PATH $PATH:/opt/spark/bin
ENV PYSPARK_PYTHON python3
ENV PYSPARK_DRIVER_PYTHON python3
###############################
## Finish SPARK files and variables
###############################
#USER airflow
#WORKDIR ${AIRFLOW_HOME}
#RUN apt-get install python3-sklearn python3-sklearn-lib python3-sklearn-doc
#RUN git clone https://github.com/catboost/catboost.git
#RUN cd catboost/catboost/python-package/catboost
#RUN ../../../ya make -r -DUSE_ARCADIA_PYTHON=no -DOS_SDK=local -DPYTHON_CONFIG=python3-config


