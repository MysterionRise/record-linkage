package org.mystic

import org.mystic.Utils._
import scala.io.Source

object SimpleWorkflow {

  def main(args: Array[String]): Unit = {
    loadData("ibm.csv")
  }

  // ids of columns
  val HIGH_id: Int = 2
  val LOW_id: Int = 3
  val VOLUME_id: Int = 5

  val volatility = (fs: Array[String]) => fs(HIGH_id).toDouble - fs(LOW_id).toDouble
  val volume = (fs: Array[String]) => fs(VOLUME_id).toDouble

  def transform(columns: Array[Array[String]]): XYTSeries = {
    val volatility = Stats[Double](columns.map(SimpleWorkflow.volatility)).normalise
    val volume = Stats[Double](columns.map(SimpleWorkflow.volume)).normalise
    volatility.zip(volume)
  }

  def loadData(fileName: String): Option[XYTSeries] = {
    val src = Source.fromFile(fileName)
    val fields = src.getLines().map(_.split(CSV_DELIM)).toArray
    val columns = fields.drop(1)
    val data = transform(columns)
    src.close
    Some(data)
  }
}
