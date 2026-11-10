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

def loc = JenkinsLocationConfiguration.get()
if (loc != null) {
    loc.setUrl(env['JENKINS_EXTERNAL_URL'] ?: 'http://localhost:8080/')
    loc.save()
}

instance.setNumExecutors(2)
instance.setSystemMessage('Mini-projet QA WebTours - Jenkins Docker (Linux)')
instance.save()
println "[init] Jenkins configure (admin, URL, 2 executeurs)"
