package org.mystic.h2h.snippet

import net.liftweb.http.DispatchSnippet
import scala.xml.{Text, NodeSeq}

class PerfomantSnippet extends DispatchSnippet{

  def dispatch: PerfomantSnippet#DispatchIt = {
    case name => render(name) _

  }

  def render (name : String)(ignore : NodeSeq) : NodeSeq =
    Text("Hello, world! Invoked as " + name)

}
