package org.mystic.h2h.fantasy

import org.slf4j.LoggerFactory
import scala.collection.mutable.ListBuffer
import org.htmlcleaner.HtmlCleaner
import java.net.URL

object PlayersCrawler {

  val logger = LoggerFactory.getLogger(getClass)
  val pagination = "?p="

  def getAllTeams(leagueURI: String): List[(String, String, String, String, Int)] = {
    var teams = new ListBuffer[(String, String, String, String, Int)]
    val cleaner = new HtmlCleaner
    var i = 1
    var flag = true
    val teamCrawler = new TeamParser
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
              val teamName = teamCrawler.nameOfTeam(teamURI)
              val cost = teamCrawler.costOfTeam(teamURI)
              val balance = teamCrawler.balanceOfTeam(teamURI)
              val totalCost = Integer.parseInt(cost.substring(4, cost.length - 5)) + Integer.parseInt(balance.substring(4, balance.length - 5))
              val userName = teamCrawler.userName(teamURI)
              teams.+=((teamURI, teamName, null, userName, totalCost))
              // teamURI, teamName, playerURI, playerName, score
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


  def getAllTeamsInLeague(leagueURI: String): List[(String, String, String, String, String)] = {
    var teams = new ListBuffer[(String, String, String, String, String)]
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(leagueURI))
    val elements = rootNode.getElementsByName("td", true)
    val teamCrawler = new TeamParser
    for (elem <- elements) {
      val classType = elem.getAttributeByName("class")
      if (classType != null && classType.equalsIgnoreCase("name-td alLeft")) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          val childClassType = childElem.getAttributeByName("class")
          if (childClassType != null && childClassType.equalsIgnoreCase("bold")) {
            val teamURI = "http://sports.ru" + childElem.getAttributeByName("href")
            val teamName = teamCrawler.nameOfTeam(teamURI)
            val cost = teamCrawler.costOfTeam(teamURI)
            val balance = teamCrawler.balanceOfTeam(teamURI)
            val userName = teamCrawler.userName(teamURI)
            val totalCost = Integer.parseInt(cost.substring(4, cost.length - 5)) + Integer.parseInt(balance.substring(4, balance.length - 5))
            teams.+=((teamURI, teamName, null, userName, totalCost.toString))
            // teamURI, teamName, playerURI, playerName, score
          }
        }
      }
    }
    teams.toList
  }
}
