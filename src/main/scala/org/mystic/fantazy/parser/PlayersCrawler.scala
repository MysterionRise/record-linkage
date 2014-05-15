package org.mystic.fantazy.parser

import org.slf4j.LoggerFactory
import scala.collection.mutable.ListBuffer
import org.htmlcleaner.{TagNode, HtmlCleaner}
import java.net.URL
import org.mystic.fantazy.domain.Team

object PlayersCrawler {

  val logger = LoggerFactory.getLogger(getClass)
  val pagination = "?p="
  val classAttr: String = "class"
  val classValue: String = "name-td alLeft"
  val site: String = "http://sports.ru"
  val href = "href"
  val td = "td"
  val bold = "bold"

  def extractTeamInfo(childElem: TagNode, teamCrawler: TeamParser, teams: ListBuffer[Team]) = {
    val teamURI = site + childElem.getAttributeByName(href)
    val team = teamCrawler.getItAll(teamURI)
    val score = team.score
    val balance = team.balance
    if (score != null && balance != null) {
      val totalCost = Integer.parseInt(score.substring(4, score.length - 5)) + Integer.parseInt(balance.substring(4, balance.length - 5))
      team.totalCost = totalCost
    }
    teams.+=(team)
  }


  def getAllTeams(leagueURI: String): List[Team] = {
    val teams = new ListBuffer[Team]
    val cleaner = new HtmlCleaner
    var i = 1
    var flag = true
    val teamCrawler = new TeamParser
    while (flag) {
      var len = 0
      val rootNode = cleaner.clean(new URL(leagueURI + pagination + i))
      val elements = rootNode.getElementsByName(td, true)
      for (elem <- elements) {
        val classType = elem.getAttributeByName(classAttr)
        if (classType != null && classType.equalsIgnoreCase(classValue)) {
          val childElements = elem.getChildTags
          for (childElem <- childElements) {
            val childClassType = childElem.getAttributeByName(classAttr)
            if (childClassType != null && childClassType.equalsIgnoreCase(bold)) {
              extractTeamInfo(childElem, teamCrawler, teams)
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


  def getAllTeamsInLeague(leagueURI: String): List[Team] = {
    val teams = new ListBuffer[Team]
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(leagueURI))
    val elements = rootNode.getElementsByName(td, true)
    val teamCrawler = new TeamParser
    for (elem <- elements) {
      val classType = elem.getAttributeByName(classAttr)
      if (classType != null && classType.equalsIgnoreCase(classValue)) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          val childClassType = childElem.getAttributeByName(classAttr)
          if (childClassType != null && childClassType.equalsIgnoreCase(bold)) {
            extractTeamInfo(childElem, teamCrawler, teams)
          }
        }
      }
    }
    teams.toList
  }

  def main(args: Array[String]) {
    val start = System.currentTimeMillis()
    val teams = getAllTeams("http://www.sports.ru/fantasy/basketball/league/10942.html")
    System.out.println(teams.length)
    System.out.println((System.currentTimeMillis() - start) / 1000)
  }
}
