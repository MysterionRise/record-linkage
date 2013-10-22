package org.mystic.h2h.fantasy

import org.slf4j.LoggerFactory
import scala.collection.mutable.ListBuffer
import org.htmlcleaner.HtmlCleaner
import java.net.URL

object PlayersCrawler {

  val logger = LoggerFactory.getLogger(getClass)
  val pagination = "?p="

  def getAllTeams(leagueURI: String): List[(String, String, Int)] = {
    var teams = new ListBuffer[(String, String, Int)]
    val cleaner = new HtmlCleaner
    var i = 1
    var flag = true
    while (flag) {
      var len = 0
      val rootNode = cleaner.clean(new URL(leagueURI + pagination + i))
      val elements = rootNode.getElementsByName("td", true)
      for (elem <- elements) {
        val classType = elem.getAttributeByName("class")
        if (classType != null && classType.equalsIgnoreCase("name-td alLeft bordR")) {
          val childElements = elem.getChildTags
          for (childElem <- childElements) {
            val childClassType = childElem.getAttributeByName("class")
            if (childClassType != null && childClassType.equalsIgnoreCase("bold")) {
              val teamURI = "http://sports.ru" + childElem.getAttributeByName("href")
              teams.+=((teamURI, null, 0))
              len += 1
            }
          }
        }
      }
      if (len == 0)
        flag = false
      i += 1
    }
    teams.toList
  }


  def getAllTeamsInLeague(leagueURI: String): List[(String, String, Int)] = {
    var teams = new ListBuffer[(String, String, Int)]
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(leagueURI))
    val elements = rootNode.getElementsByName("td", true)
    for (elem <- elements) {
      val classType = elem.getAttributeByName("class")
      if (classType != null && classType.equalsIgnoreCase("name-td alLeft")) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          val childClassType = childElem.getAttributeByName("class")
          if (childClassType != null && childClassType.equalsIgnoreCase("bold")) {
            val teamURI = "http://sports.ru" + childElem.getAttributeByName("href")
            teams.+=((teamURI, null, 0))
          }
        }
      }
    }
    teams.toList
  }
}
