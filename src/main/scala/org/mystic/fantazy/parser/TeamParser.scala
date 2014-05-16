package org.mystic.fantazy.parser

import org.slf4j.LoggerFactory
import org.mystic.fantazy.domain.Team
import org.htmlcleaner.HtmlCleaner
import java.net.URL

/**
 * Crawling team info from sports.ru
 */
class TeamParser {

  val logger = LoggerFactory.getLogger(getClass)
  val th = "th"
  val classAttr = "class"
  val classValue = "profile-table"

  def getItAll(teamURI: String): Team = {
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(teamURI))
    val elements = rootNode.getElementsByName(th, true)
    for (elem <- elements) {
      val classType = elem.getAttributeByName(classAttr)
      if (classType != null && classType.equalsIgnoreCase(classValue)) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          childElem.getNam
          if (childElem.getName)
          if (childClassType != null && childClassType.equalsIgnoreCase(bold)) {
            extractTeamInfo(childElem, teamCrawler, teams)
            len += 1
          }
        }
      }
    }
    val url = new java.net.URL(teamURI)
    val scan = new java.util.Scanner(url.openStream, "UTF-8")
    // teamURI, teamName, playerURI, playerName, score, bal
    while (scan.hasNext) {
      val s = scan.nextLine
      if (s.contains("<th>Пользователь</th>")) {
        val str: String = scan.nextLine.substring(48)
        val playerName = str.substring(0, str.length - 9).replace(">", "").replace("\"", "")
      }
      if (s.contains("<title>")) {
        val teamName = s.substring(7, s.length - ": профиль - Фэнтези - Sports.ru</title>".length)
      }
      if (s.contains("<th>Стоимость команды</th>")) {
        val score = scan.nextLine
      }
      if (s.contains("<th>Баланс</th>")) {
        val balance = scan.nextLine
      }
    }
    new Team(teamName, teamURI, playerName, score, balance, 0)
  }
}