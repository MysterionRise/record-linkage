package org.mystic

trait PipeOperator[-T, +U] {

  def |>(data: T): Option[U]
}
