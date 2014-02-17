package org.mystic.h2h.fantasy

/**
 * @author kperikov
 */
object LeagueManipulation {

  def readAvailiableLeagues: Unit = {

  }

  def writeHtmlLeagues: Array[(String, String)] = {
    val arr: Array[(String, String)] = new Array[(String, String)](numberOfLeagues)
    arr(0) = ("H2H NBA 2013/2014 DIV1", "h2h-nba-div1")
    arr(1) = ("H2H NBA 2013/2014 DIV2", "h2h-nba-div2")
    arr
  }

  def numberOfLeagues: Int = {
    2
  }

}
