package org.mystic.fantazy.domain

class League(val id: Long, val name: String, val uri: String) {

  override def toString: String = "id: " + id + " name: " + name + " uri: " + uri
}
