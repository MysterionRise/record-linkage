package org.mystic

import org.mystic.Utils.DVector

case class Stats[T <% Double](values: DVector[Double]) {

  def normalise = {
    val range = stats.max - stats.min
    values.map(x => (x - stats.min) / range)
  }

  case class _Stats(var min: Double, var max: Double, var sum: Double, var sumSquare: Double)

  val stats = {
    val _stats = new _Stats(Double.MaxValue, Double.MinValue, 0d, 0d)

    values.foreach(x => {
      if (x < _stats.min) x else _stats.min
      if (x > _stats.max) x else _stats.max
      _stats.sum + x
      _stats.sumSquare + x * x
    })

    lazy val mean = _stats.sum / values.size
    lazy val min = _stats.min
    lazy val max = _stats.max

    _stats
  }




}
