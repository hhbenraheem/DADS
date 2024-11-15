# DADS6005 - Take-home Midterm Exam
This repository contains the code, configurations, and documentation for the DADS6005 take-home midterm exam. The project focuses on building a data streaming and real-time analytics system using AWS, Apache Kafka, ksqlDB, Apache Pinot, and Streamlit. It fulfills the requirements for data generation, stream processing, storage, and dashboard creation.

## Overview
The objective of this project is to implement a real-time data streaming and analytics system that handles multiple data sources and provides a dashboard for visual insights. The system comprises data generation, Kafka-based streaming, data transformation with ksqlDB, and interactive visualization using Streamlit.

## Components and Workflow
1. **Kafka & ksqlDB**: 
   - Kafka serves as the core data streaming system with multi-partitioned topics.
   - ksqlDB processes and transforms data streams, performing filtering, joining, and aggregating as specified in the requirements​.
2. **Apache Pinot**: 
   - Apache Pinot is used for real-time OLAP analytics, storing data from ksqlDB streams and enabling fast querying for dashboard visualizations.
3. **Streamlit Dashboard**:
   - An interactive dashboard visualizes metrics such as PageView counts, user demographics, and regional data aggregations using panels powered by Apache Pinot queries.
   - Here is an overview of the real-time data analytics dashboard:

![Dashboard Overview](https://i.ibb.co/tHFjktM/Streamlit-Dashboard.png)

You can view the live dashboard at http://ec2-122-248-218-143.ap-southeast-1.compute.amazonaws.com:8501/
