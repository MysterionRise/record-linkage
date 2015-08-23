package com.github.mysterionrise

import org.apache.spark.{SparkConf, SparkContext}

object NBAPrediction {
  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("My Own Spark Application!")
    val spark = new SparkContext(conf)
    spark.stop()
  }
}
