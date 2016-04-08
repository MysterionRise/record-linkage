package org.mystic

object Utils {
  type XY = (Double, Double)
  type XYTSeries = Array[XY]
  type DVector[T] = Array[T]
  type DMatrix[T] = Array[Array[T]]
  type DoubleMatrix = DMatrix[Double]
  type DoubleVector = DVector[Double]

  implicit def int2double(i: Int): Double = i.toDouble

  implicit def vectorT2DoubleVector[T <% Double](v: DVector[T]): DoubleVector = v.map(_.toDouble)

  implicit def double2DoubleVector(d: Double) = Array[Double](d)
}
