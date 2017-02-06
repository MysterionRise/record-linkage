package org.mystic.cache

import java.util.concurrent.TimeUnit

import com.hazelcast.client.HazelcastClient
import com.hazelcast.core.{Hazelcast, IMap}

import scala.util.Random

object Client {

  def main(args: Array[String]): Unit = {
    val hz = HazelcastClient.newHazelcastClient()
    val skus: IMap[Int, Int] = hz.getMap("skus")

    val rand = new Random()
    while (true) {
      val skuToBuy = rand.nextInt(SKU_SIZE)
      var flag = true
      while (flag) {
        val oldValue = skus.get(skuToBuy)
        val ammountToBuy = rand.nextInt(oldValue / 10 + 1)
        val newValue = oldValue - ammountToBuy
        if (skus.replace(skuToBuy, oldValue, newValue)) {
          println(s"buying $skuToBuy $ammountToBuy")
          flag = false
        }
      }
      TimeUnit.MILLISECONDS.sleep(200)
    }
  }
}
