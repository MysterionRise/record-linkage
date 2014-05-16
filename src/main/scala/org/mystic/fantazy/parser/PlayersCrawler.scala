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

  def extractTeamInfo(childElem: TagNode, teams: ListBuffer[Team]) = {
    val teamURI = site + childElem.getAttributeByName(href)
    val team = TeamParser.getTeamSummary(teamURI)
    teams.+=(team)
  }


  def getAllTeams(leagueURI: String): List[Team] = {
    val teams = new ListBuffer[Team]
    var pageNumber = 1
    var prevLength = -1
    while (teams.length - prevLength > 0) {
      prevLength = teams.length
      getAllTeamsOnPage(leagueURI, pageNumber, teams)
      pageNumber += 1
    }
    teams.toList
  }

  def getAllTeamsOnPage(leagueURI: String, pageNumber: Int, teams: ListBuffer[Team]) = {
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(leagueURI + pagination + pageNumber))
    val elements = rootNode.getElementsByName(td, true)
    for (elem <- elements) {
      val classType = elem.getAttributeByName(classAttr)
      if (classType != null && classType.equalsIgnoreCase(classValue)) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          val childClassType = childElem.getAttributeByName(classAttr)
          if (childClassType != null && childClassType.equalsIgnoreCase(bold)) {
            extractTeamInfo(childElem, teams)
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
    System.out.println((System.currentTimeMillis() - start) + " ms")
  }
}
