package org.mystic.cache

import com.hazelcast.client.HazelcastClient
import com.hazelcast.core.IMap

import scala.util.Random

object PopulatingClient {

  def main(args: Array[String]): Unit = {
    val hz = HazelcastClient.newHazelcastClient()
    val skus: IMap[Int, Int] = hz.getMap("skus")

    val rand = new Random()
    while (true) {
      for (i <- 0 until OPERATIONS) {
        val sku = rand.nextInt(SKU_SIZE)
        val availability = rand.nextInt(AVAILABILITY_SIZE) + skus.getOrDefault(sku, 0)
        skus.put(sku, availability)
        println(s"$sku $availability")
      }
      println(s"sleeping... ${System.currentTimeMillis() / 1000}")
      Thread.sleep(60 * 1000 * 5)
    }
  }
}
