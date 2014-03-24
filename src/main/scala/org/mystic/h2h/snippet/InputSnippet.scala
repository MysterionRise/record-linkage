package org.mystic.h2h.snippet

import net.liftweb.http.DispatchSnippet
import scala.xml.{Text, NodeSeq}

class InputSnippet extends DispatchSnippet{
  def dispatch: InputSnippet#DispatchIt = {
    case name => render(name) _
  }

  def render (name : String)(input : NodeSeq) : NodeSeq =
    Text("Hello, world! Invoked as " + name + "with input " + input)
}
