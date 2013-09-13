package org.mystic.h2h.fantasy

/**
 * @author kperikov
 */
object LeagueManipulation {

  def readAvailiableLeagues: Unit = {

  }

  def writeHtmlLeagues: Array[(String, String)] = {
    val arr: Array[(String, String)] = new Array[(String, String)](numberOfLeagues)
    arr(0) = ("H2H NBA 2013/2014", "h2h-nba")
    arr(1) = ("H2H KHL 2013/2014", "h2h-khl")
    arr
  }

  def numberOfLeagues: Int = {
    2
  }

}
