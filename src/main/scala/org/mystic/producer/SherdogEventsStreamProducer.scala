package org.mystic.producer

import org.jsoup.Jsoup
import org.jsoup.nodes.{Document, Element}
import org.jsoup.select.Elements

class SherdogEventsStreamProducer extends KafkaStreamProducer {

  override def runStream(): Unit = {
    val doc = Jsoup.connect("http://www.sherdog.com/events")
      .userAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0")
      .timeout(0)
      .get()
    val upcomingEvents = getEvents(doc, "upcoming_tab")
    val pastEvents = getEvents(doc, "recentfights_tab")

  }

  def getEvents(doc: Document, eventsId: String): Array[Event] = {
    val events = doc.getElementsByAttributeValue("id", eventsId).get(1).child(0).child(0).children()
    // ignore header
    val transformedEvents = new Array[Event](events.size() - 1)
    for (i <- 1 until events.size()) {
      transformedEvents(i - 1) = transformHTMLToEvent(events.get(i).children())
    }
    transformedEvents
  }

  def transformHTMLToEvent(elements: Elements): Event = {
    val date = elements.get(0).child(0).attr("content")
    val name = elements.get(1).child(0).attr("content")
    val title = elements.get(2).child(0).text()
    val link = elements.get(2).child(0).attr("href")
    val location = elements.get(3).child(1).text()
    Event(name, title, link, date, location)
  }

  case class Event(name: String, title: String, link: String, date: String, location: String)

}
