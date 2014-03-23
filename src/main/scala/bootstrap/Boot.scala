package bootstrap.liftweb

import net.liftweb.http.{Html5Properties, LiftRules, Req}
import net.liftweb.sitemap.{Menu, SiteMap}

/**
 * A class that's instantiated early and run.  It allows the application
 * to modify lift's environment
 */
class Boot {
  def boot {
    // where to search snippet
    LiftRules.addToPackages("org.mystic.h2h")

    // Build SiteMap
    def sitemap(): SiteMap = SiteMap(
      Menu.i("Home") / "index",

    Menu.i("Info") / "info" submenus(
      Menu.i("About") / "about",
      Menu.i("Contact") / "contact",
      Menu.i("Feedback") / "feedback")
    )

    LiftRules.setSiteMapFunc(() => sitemap())

    // @todo HTML5 ruins snippet detection
//    LiftRules.htmlProperties.default.set((r: Req) =>
//      new Html5Properties(r.userAgent))
  }
}