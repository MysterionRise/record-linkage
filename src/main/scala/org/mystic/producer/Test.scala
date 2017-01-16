package org.mystic.producer

import java.util.Properties
import scalaj.http._

import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}

object Test {

  def main(args: Array[String]): Unit = {
    /*val props = new Properties()
    props.put("bootstrap.servers", "localhost:9092")

    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)*/

    val TOPIC = "test"

    Http("http://stream.meetup.com/2/rsvps").execute(is => {
      scala.io.Source.fromInputStream(is).getLines().foreach(lines => {
        println(lines)
        val record = new ProducerRecord(TOPIC, "key", s"$lines")
        //producer.send(record)
      })
    })

    //producer.close()

  }

}
