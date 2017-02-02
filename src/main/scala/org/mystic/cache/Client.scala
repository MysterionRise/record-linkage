package org.mystic.cache

import com.hazelcast.client.HazelcastClient
import com.hazelcast.core.{Hazelcast, IMap}

import scala.util.Random

object Client {

  def main(args: Array[String]): Unit = {
    val hz = HazelcastClient.newHazelcastClient()
    val skus: IMap[Int, Int] = hz.getMap("skus")

    val rand = new Random()
    while (true) {
      for (i <- 0 until rand.nextInt(BUYING_OPERATIONS)) {
        val skuToBuy = rand.nextInt(SKU_SIZE)
        if (skus.containsKey(skuToBuy)) {
          val tryToBuy = rand.nextInt(AVAILABILITY_SIZE / 10)
          val ammount = skus.get(skuToBuy)
          if (ammount >= tryToBuy) {
            skus.put(skuToBuy, ammount - tryToBuy)
            println(s"buying $skuToBuy $tryToBuy")
          }
        }
      }
      println(s"sleeping...${System.currentTimeMillis() / 1000}")
      Thread.sleep(rand.nextInt(100000))
    }
  }
}
