package org.mystic

import java.io.File

import org.jfree.chart.plot.PlotOrientation
import org.jfree.chart.{ChartFactory, ChartUtilities}
import org.jfree.data.xy.{XYSeries, XYSeriesCollection}
import org.mystic.Utils._

import scala.io.Source

object SimpleWorkflow {

  def plotData(data: Option[XYTSeries]) = {
    val xLegend = "Volatility"
    val yLegend = "Volume"
    val series = new XYSeries("IBM stocks")
    data.getOrElse(new XYTSeries(0)).foreach(x => series.add(x._1, x._2))
    val seriesCollection = new XYSeriesCollection(series)
    val chart = ChartFactory.createScatterPlot(xLegend, xLegend, yLegend, seriesCollection, PlotOrientation.VERTICAL, true, false, false)
    ChartUtilities.saveChartAsPNG(new File("test.png"), chart, 1024, 768)
  }

  def makePrediction: Unit = ???

  def main(args: Array[String]): Unit = {
    val data = loadData("ibm-old-data.csv")
    plotData(data)
    makePrediction
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
    try {
      val src = Source.fromFile(fileName)
      val fields = src.getLines().map(_.split(CSV_DELIM)).toArray
      val columns = fields.drop(1)
      val data = transform(columns)
      src.close
      Some(data)
    } catch {
      case e: Exception => None
    }
  }
}
