package org.mystic.h2h.snippet

import net.liftweb.http.{DispatchSnippet, S}
import scala.xml.NodeSeq

class HelloWorld extends DispatchSnippet {

  def helloLift(xhtml: NodeSeq) =
    <span>Welcome to H2H Fantazy at
      {new _root_.java.util.Date}
    </span>

  def dispatch: HelloWorld#DispatchIt = {
    case "howdy" => helloLift _
    case _ => catchAll _
  }

  def catchAll(xhtml: NodeSeq) =
    <span>Something unexpected is requested
    </span>
}
