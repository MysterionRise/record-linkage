package org.mystic

import org.mystic.Utils._
import scala.io.Source

object SimpleWorkflow {

  def main(args: Array[String]): Unit = {
    loadData("ibm.csv")
  }

  def transform(columns: Array[Array[String]]) = ???

  def loadData(fileName: String): Option[XYTSeries] = {
    val src = Source.fromFile(fileName)
    val fields = src.getLines().map(_.split(CSV_DELIM)).toArray
    val columns = fields.drop(1)
    val data = transform(columns)
    src.close
    Some(data)
  }
}
