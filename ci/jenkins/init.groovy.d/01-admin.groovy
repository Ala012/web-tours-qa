import jenkins.model.*
import hudson.security.*

def env = System.getenv()
def instance = Jenkins.get()

def password = env['JENKINS_ADMIN_PASSWORD']
if (password) {
    def realm = instance.getSecurityRealm()
    if (!(realm instanceof HudsonPrivateSecurityRealm)) {
        realm = new HudsonPrivateSecurityRealm(false)
        instance.setSecurityRealm(realm)
    }
    if (realm.getUser('admin') == null) {
        realm.createAccount('admin', password)
        println "[init] Compte admin cree"
    }
    def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
    strategy.setAllowAnonymousRead(false)
    instance.setAuthorizationStrategy(strategy)
}

instance.setLabelString('windows built-in master')
instance.setSystemMessage('Mini-projet QA WebTours - pipeline Selenium/pytest')
instance.save()
println "[init] Jenkins configure (label windows, securite admin)"
