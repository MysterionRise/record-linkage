package org.mystic.fantazy.domain

/**
 * DTO for saving team properties
 */
// teamURI, teamName, playerURI, playerName, score, bal and awesome summary info
class Team(val name: String, val uri: String, val playerName: String, var totalCost: Int, val summaryInfo: String) {

  override def toString(): String = {
    playerName + " " + totalCost
  }
}
