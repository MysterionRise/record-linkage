package org.mystic.fantazy.parser

import org.slf4j.LoggerFactory
import org.mystic.fantazy.domain.Team
import org.htmlcleaner.HtmlCleaner
import java.net.URL
import scala.StringBuilder

/**
 * Crawling team info from sports.ru
 */
object TeamParser {

  val logger = LoggerFactory.getLogger(getClass)
  val table = "table"
  val classAttr = "class"
  val classValue = "profile-table"

  def getTeamSummary(teamURI: String): Team = {
    val cleaner = new HtmlCleaner
    val rootNode = cleaner.clean(new URL(teamURI))
    val elements = rootNode.getElementsByName(table, true)
    val summary = new StringBuilder
    for (elem <- elements) {
      val classType = elem.getAttributeByName(classAttr)
      if (classType != null && classType.equalsIgnoreCase(classValue)) {
        val childElements = elem.getChildTags
        for (childElem <- childElements) {
          summary.append(childElem.getText.toString.replaceAll("\\s{2,}", " "))
        }
      }
    }
    createTeam(summary, teamURI)
  }

  def createTeam(summary: StringBuilder, teamURI: String): Team = {
    val parsebleInfo: String = summary.toString.replaceAll("\\s{1,}", " ").trim
    //    System.out.println(parsebleInfo)
    val playerNameStart = parsebleInfo.lastIndexOf("Пользователь") + 1 + "Пользователь".length
    val playerNameEnd = parsebleInfo.lastIndexOf("Турнир") - 1
    //    System.out.println(parsebleInfo.substring(playerNameStart, playerNameEnd))
    val scoreStart = parsebleInfo.lastIndexOf("Стоимость команды") + 1 + "Стоимость команды".length
    val scoreEnd = parsebleInfo.lastIndexOf("Баланс") - 1
    //    System.out.println(parsebleInfo.substring(scoreStart, scoreEnd))
    val balanceStart = scoreEnd + "Баланс".length + 2
    val balanceEnd = parsebleInfo.lastIndexOf("Трансферы") - 1
    //    System.out.println(parsebleInfo.substring(balanceStart, balanceEnd))
    val totalCost = Integer.parseInt(parsebleInfo.substring(scoreStart, scoreEnd)) + Integer.parseInt(parsebleInfo.substring(balanceStart, balanceEnd))
    //    System.out.println(totalCost)
    // TODO we could parse multiple stuff like place, number of transfers, etc.
    new Team(null, teamURI, parsebleInfo.substring(playerNameStart, playerNameEnd), totalCost, summary.toString())
  }

  def main(args: Array[String]) {
    val start = System.currentTimeMillis()
    getTeamSummary("http://sports.ru/fantasy/basketball/team/309963.html")
    System.out.println((System.currentTimeMillis() - start) + " ms")
  }
}